const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../sw.js'), 'utf8');
function setup() {
  const listeners = {}, store = new Map(), deleted = [], calls = [];
  let network = async () => new Response('fresh'), failPut = false;
  const key = request => typeof request === 'string' ? request : request.url;
  const cache = {
    match: async request => store.get(key(request))?.clone(),
    put: async (request, response) => { if (failPut) throw Error('quota'); store.set(key(request), response.clone()); },
    addAll: async () => {},
  };
  vm.runInNewContext(source, {
    URL, Response,
    self: { location: { origin: 'https://novagenai.com.my' }, addEventListener: (name, listener) => listeners[name] = listener, skipWaiting() {}, clients: { claim: async () => {} } },
    caches: { match: cache.match, open: async () => cache, keys: async () => ['novagenai-v2', 'novagenai-v3', 'other-app'], delete: async name => deleted.push(name) },
    fetch: async (...args) => { calls.push(args); return network(...args); },
  });
  return {
    store, deleted, calls,
    setNetwork: handler => network = handler,
    failPut: () => failPut = true,
    activate: async () => { let work; listeners.activate({ waitUntil: promise => work = promise }); await work; },
    run: async (url, { method = 'GET', mode = 'navigate', accept = 'text/html' } = {}) => {
      let response;
      const pending = [];
      listeners.fetch({ request: { url, method, mode, headers: new Headers({ accept }) }, respondWith: promise => response = promise, waitUntil: promise => pending.push(promise) });
      const result = await response;
      await Promise.all(pending);
      return result;
    },
  };
}
const home = 'https://novagenai.com.my/';
test('online HTML is fresh and revalidates HTTP cache', async () => {
  const h = setup(); h.store.set(home, new Response('old'));
  assert.equal(await (await h.run(home)).text(), 'fresh');
  assert.equal(await h.store.get(home).text(), 'fresh');
  assert.equal(h.calls[0][1].cache, 'no-cache');
});
test('offline exact URL returns cached document', async () => {
  const h = setup(); h.store.set(home, new Response('saved')); h.setNetwork(async () => { throw Error('offline'); });
  assert.equal(await (await h.run(home)).text(), 'saved');
});
test('offline uncached page returns 503, not unrelated homepage', async () => {
  const h = setup(); h.store.set(home, new Response('saved')); h.setNetwork(async () => { throw Error('offline'); });
  const result = await h.run(home + 'contact.html');
  assert.equal(result.status, 503);
  assert.match(await result.text(), /offline/i);
});
test('HTTP 404 is not masked or stored', async () => {
  const h = setup(); h.store.set(home, new Response('old')); h.setNetwork(async () => new Response('gone', { status: 404 }));
  assert.equal((await h.run(home)).status, 404);
  assert.equal(await h.store.get(home).text(), 'old');
});
test('assets remain stale while revalidating', async () => {
  const h = setup(), url = home + 'style.css'; h.store.set(url, new Response('old css'));
  assert.equal(await (await h.run(url, { mode: 'cors', accept: 'text/css' })).text(), 'old css');
  assert.equal(await h.store.get(url).text(), 'fresh');
});
test('cross origin, POST, and media pass through', async () => {
  const h = setup();
  assert.equal(await h.run('https://other.invalid/image.png'), undefined);
  assert.equal(await h.run(home, { method: 'POST' }), undefined);
  assert.equal(await h.run(home + 'demo.mp4', { mode: 'cors', accept: 'video/mp4' }), undefined);
  assert.equal(h.calls.length, 0);
});
test('activate deletes only older NovaGenAI cache', async () => {
  const h = setup(); await h.activate(); assert.deepEqual(h.deleted, ['novagenai-v2']);
});
test('quota failure does not hide successful network content', async () => {
  const h = setup(); h.failPut(); assert.equal(await (await h.run(home)).text(), 'fresh');
});
test('offline uncached asset returns a network error response', async () => {
  const h = setup(); h.setNetwork(async () => { throw Error('offline'); });
  const result = await h.run(home + 'new.js', { mode: 'cors', accept: 'application/javascript' });
  assert.equal(result.type, 'error');
});
