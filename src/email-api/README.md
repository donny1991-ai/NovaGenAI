# NovaGenAI Email API

Azure Functions microservice for the NovaGenAI website contact form.

## Endpoint

`POST /api/contact`

Expected JSON:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+60 12-345 6789",
  "company": "Example Sdn Bhd",
  "address": "Cyberjaya",
  "industry": "Healthcare",
  "message": "I want to discuss an AI project.",
  "source": "website-contact-form"
}
```

## Required Azure app settings

The Function reads all mail configuration from Function App environment variables:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_SECURE`
- `SMTP_USER`
- `SMTP_PASS`
- `MAIL_FROM`
- `MAIL_TO`

Set these directly in Azure Portal:

Function App > Settings > Environment variables > App settings

Or set them with Azure CLI:

```bash
az functionapp config appsettings set \
  --resource-group "$(azd env get-value AZURE_RESOURCE_GROUP)" \
  --name "$(azd env get-value AZURE_FUNCTION_APP_NAME)" \
  --settings \
    SMTP_HOST="<smtp-host>" \
    SMTP_PORT="587" \
    SMTP_SECURE="false" \
    SMTP_USER="<smtp-user>" \
    SMTP_PASS="<smtp-password>" \
    MAIL_FROM="NovaGenAI Website <enquiries@novagenai.com.my>" \
    MAIL_TO="enquiries@novagenai.com.my"
```

## Deploy

```bash
azd up
```

After provisioning, update `contact-config.js` with the `CONTACT_API_URL` output, then deploy the static site to GitHub Pages.
