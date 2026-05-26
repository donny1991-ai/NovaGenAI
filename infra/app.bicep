param environmentName string
param location string = resourceGroup().location
param allowedOrigins array

var normalizedEnvironmentName = replace(toLower(environmentName), '-', '')
var uniqueSuffix = uniqueString(subscription().id, resourceGroup().id, environmentName)
var storageAccountName = take('st${normalizedEnvironmentName}${uniqueSuffix}', 24)
var functionAppName = take('func-${environmentName}-email-${uniqueSuffix}', 60)
var appServicePlanName = 'asp-${environmentName}-email'

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'functionapp'
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  tags: {
    'azd-env-name': environmentName
    'azd-service-name': 'email-api'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      cors: {
        allowedOrigins: allowedOrigins
        supportCredentials: false
      }
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storage.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storage.listKeys().keys[0].value}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'node'
        }
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '~20'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        {
          name: 'ALLOWED_ORIGINS'
          value: join(allowedOrigins, ',')
        }
        {
          name: 'MAIL_TO'
          value: 'enquiries@novagenai.com.my'
        }
        {
          name: 'MAIL_FROM'
          value: 'NovaGenAI Website <enquiries@novagenai.com.my>'
        }
        {
          name: 'SMTP_PORT'
          value: '587'
        }
        {
          name: 'SMTP_SECURE'
          value: 'false'
        }
      ]
    }
  }
}

output functionAppName string = functionApp.name
output contactApiUrl string = 'https://${functionApp.properties.defaultHostName}/api/contact'
