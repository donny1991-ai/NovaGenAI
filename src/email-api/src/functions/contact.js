const { app } = require('@azure/functions');
const nodemailer = require('nodemailer');

const DEFAULT_ORIGINS = [
  'https://novagenai.com.my',
  'https://www.novagenai.com.my',
  'http://localhost:8080',
  'http://127.0.0.1:8080',
];
const MAX_REQUEST_BYTES = 32 * 1024;

function getAllowedOrigins() {
  return (process.env.ALLOWED_ORIGINS || DEFAULT_ORIGINS.join(','))
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean);
}

function getCorsHeaders(request) {
  const origin = request.headers.get('origin');
  const allowedOrigins = getAllowedOrigins();
  const headers = {
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    Vary: 'Origin',
  };

  if (origin && allowedOrigins.includes(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
  }

  return headers;
}

function jsonResponse(request, status, body) {
  return {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...getCorsHeaders(request),
    },
    jsonBody: body,
  };
}

function clean(value, fallback = '') {
  return String(value || fallback).trim().slice(0, 2000);
}

function cleanHeader(value, fallback = '') {
  return clean(value, fallback).replace(/[\r\n]+/g, ' ').slice(0, 200);
}

function validatePayload(payload) {
  const required = ['name', 'email', 'phone', 'message'];
  const missing = required.filter((field) => !clean(payload[field]));

  if (missing.length > 0) {
    return `Missing required fields: ${missing.join(', ')}`;
  }

  const email = clean(payload.email);
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return 'Invalid email address';
  }

  const phoneDigits = clean(payload.phone).replace(/\D/g, '');
  if (phoneDigits.length < 8) {
    return 'Invalid phone number';
  }

  return null;
}

function requireConfig(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing app setting: ${name}`);
  }
  return value;
}

function createTransporter() {
  if (String(process.env.EMAIL_DRY_RUN || 'false').toLowerCase() === 'true') {
    return nodemailer.createTransport({
      jsonTransport: true,
    });
  }

  const secure = String(process.env.SMTP_SECURE || 'false').toLowerCase() === 'true';

  return nodemailer.createTransport({
    host: requireConfig('SMTP_HOST'),
    port: Number(process.env.SMTP_PORT || 587),
    secure,
    auth: {
      user: requireConfig('SMTP_USER'),
      pass: requireConfig('SMTP_PASS'),
    },
  });
}

function renderTextEmail(payload) {
  return [
    'New NovaGenAI contact form submission',
    '',
    `Name: ${clean(payload.name)}`,
    `Email: ${clean(payload.email)}`,
    `Phone: ${clean(payload.phone)}`,
    `Company: ${clean(payload.company, 'Not provided')}`,
    `Address: ${clean(payload.address, 'Not provided')}`,
    `Industry: ${clean(payload.industry, 'Not specified')}`,
    `Source: ${clean(payload.source, 'website-contact-form')}`,
    `Submitted: ${clean(payload.timestamp, new Date().toISOString())}`,
    '',
    'Message:',
    clean(payload.message),
  ].join('\n');
}

function renderHtmlEmail(payload) {
  const rows = [
    ['Name', clean(payload.name)],
    ['Email', clean(payload.email)],
    ['Phone', clean(payload.phone)],
    ['Company', clean(payload.company, 'Not provided')],
    ['Address', clean(payload.address, 'Not provided')],
    ['Industry', clean(payload.industry, 'Not specified')],
    ['Source', clean(payload.source, 'website-contact-form')],
    ['Submitted', clean(payload.timestamp, new Date().toISOString())],
  ];

  const escapeHtml = (value) =>
    value.replace(/[&<>"']/g, (char) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    }[char]));

  return `
    <h2>New NovaGenAI contact form submission</h2>
    <table cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-family:Arial,sans-serif;">
      ${rows.map(([label, value]) => `
        <tr>
          <th align="left" style="border-bottom:1px solid #ddd;">${escapeHtml(label)}</th>
          <td style="border-bottom:1px solid #ddd;">${escapeHtml(value)}</td>
        </tr>
      `).join('')}
    </table>
    <h3>Message</h3>
    <p style="white-space:pre-wrap;font-family:Arial,sans-serif;">${escapeHtml(clean(payload.message))}</p>
  `;
}

app.http('contact', {
  methods: ['POST', 'OPTIONS'],
  authLevel: 'anonymous',
  route: 'contact',
  handler: async (request, context) => {
    if (request.method === 'OPTIONS') {
      return {
        status: 204,
        headers: getCorsHeaders(request),
      };
    }

    const origin = request.headers.get('origin');
    const allowedOrigins = getAllowedOrigins();
    if (origin && !allowedOrigins.includes(origin)) {
      return jsonResponse(request, 403, { ok: false, error: 'Origin is not allowed' });
    }

    const contentLength = Number(request.headers.get('content-length') || 0);
    if (contentLength > MAX_REQUEST_BYTES) {
      return jsonResponse(request, 413, { ok: false, error: 'Request body is too large' });
    }

    let payload;
    try {
      payload = await request.json();
    } catch (error) {
      return jsonResponse(request, 400, { ok: false, error: 'Request body must be valid JSON' });
    }

    const validationError = validatePayload(payload);
    if (validationError) {
      return jsonResponse(request, 400, { ok: false, error: validationError });
    }

    try {
      const transporter = createTransporter();
      await transporter.sendMail({
        from: requireConfig('MAIL_FROM'),
        to: requireConfig('MAIL_TO'),
        replyTo: clean(payload.email),
        subject: `NovaGenAI contact form: ${cleanHeader(payload.name)}`,
        text: renderTextEmail(payload),
        html: renderHtmlEmail(payload),
      });

      return jsonResponse(request, 200, { ok: true });
    } catch (error) {
      context.error('Failed to send contact email', error);
      return jsonResponse(request, 500, { ok: false, error: 'Email could not be sent' });
    }
  },
});
