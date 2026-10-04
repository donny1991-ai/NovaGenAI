const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../src/email-api/src/functions/contact.js'), 'utf8');
const good = { name: 'Local test', email: 'test@example.invalid', phone: '+60 12345678', message: 'Local only' };
function harness(failMail = false) {
  let handler;
  const sent = [];
  vm.runInNewContext(source, {
    Buffer,
    process: { env: { EMAIL_DRY_RUN: 'true', MAIL_FROM: 'from@example.invalid', MAIL_TO: 'to@example.invalid' } },
    require: name => name === '@azure/functions'
      ? { app: { http: (_, options) => { handler = options.handler; } } }
      : { createTransport: () => ({ sendMail: async message => { if (failMail) throw Error('mock failure'); sent.push(message); } }) },
  });
  return { sent, call: async (body, headers = {}, method = 'POST') => handler({
    method,
    headers: new Headers(headers),
    body: body === undefined ? null : new ReadableStream({ start(controller) {
      const data = Buffer.from(body);
      for (let i = 0; i < data.length; i += 1000) controller.enqueue(data.subarray(i, i + 1000));
      controller.close();
    } }),
  }, { error() {} }) };
}
test('valid input escapes HTML, cleans subject, and keeps fixed recipient', async () => {
  const h = harness();
  const result = await h.call(JSON.stringify({ ...good, name: 'Test\r\nSubject', message: '<script>bad</script>' }));
  assert.equal(result.status, 200);
  assert.equal(h.sent.length, 1);
  assert.equal(h.sent[0].to, 'to@example.invalid');
  assert.ok(h.sent[0].html.includes('&lt;script&gt;'));
  assert.ok(!h.sent[0].subject.includes('\n'));
});
test('invalid JSON and empty body return 400', async () => {
  for (const body of ['{', undefined]) assert.equal((await harness().call(body)).status, 400);
});
test('null, arrays, primitives, and typed fields return 400', async () => {
  for (const value of [null, [], 3, true, 'text', { ...good, name: {} }, { ...good, company: null }]) {
    assert.equal((await harness().call(JSON.stringify(value))).status, 400, String(value));
  }
});
test('missing and malformed contact values return 400', async () => {
  for (const value of [{}, { ...good, email: 'bad' }, { ...good, phone: '123' }, { ...good, message: '   ' }, { ...good, message: 'x'.repeat(2001) }]) {
    assert.equal((await harness().call(JSON.stringify(value))).status, 400);
  }
});
test('actual bytes enforce 32KiB even with missing or false Content-Length', async () => {
  for (const headers of [{}, { 'content-length': '1' }, { 'content-length': 'garbage' }]) {
    assert.equal((await harness().call(JSON.stringify({ ...good, extra: 'x'.repeat(33000) }), headers)).status, 413);
  }
  assert.equal((await harness().call(JSON.stringify(good), { 'content-length': '40000' })).status, 413);
});
test('UTF8 byte size and exact boundary', async () => {
  const start = JSON.stringify({ ...good, extra: '' });
  const exact = start.replace('"extra":""', '"extra":"' + 'x'.repeat(32768 - Buffer.byteLength(start)) + '"');
  assert.equal(Buffer.byteLength(exact), 32768);
  assert.equal((await harness().call(exact)).status, 200);
  assert.equal((await harness().call(exact + ' ')).status, 413);
  assert.equal((await harness().call(JSON.stringify({ ...good, extra: '界'.repeat(11000) }))).status, 413);
});
test('CORS preflight, denied origin, and mocked mail failure', async () => {
  const h = harness();
  assert.equal((await h.call(undefined, {}, 'OPTIONS')).status, 204);
  assert.equal((await h.call(JSON.stringify(good), { origin: 'https://other.invalid' })).status, 403);
  const ok = await h.call(JSON.stringify(good), { origin: 'https://novagenai.com.my' });
  assert.equal(ok.headers['Access-Control-Allow-Origin'], 'https://novagenai.com.my');
  assert.equal((await harness(true).call(JSON.stringify(good))).status, 500);
});
