targetScope = 'subscription'

@minLength(1)
param environmentName string

@minLength(1)
param location string

param allowedOrigins array = [
  'https://novagenai.com.my'
  'https://www.novagenai.com.my'
  'http://localhost:8080'
  'http://127.0.0.1:8080'
]

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
}

module emailApi 'app.bicep' = {
  name: 'email-api'
  scope: rg
  params: {
    environmentName: environmentName
    location: location
    allowedOrigins: allowedOrigins
  }
}

output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_LOCATION string = location
output AZURE_FUNCTION_APP_NAME string = emailApi.outputs.functionAppName
output CONTACT_API_URL string = emailApi.outputs.contactApiUrl
