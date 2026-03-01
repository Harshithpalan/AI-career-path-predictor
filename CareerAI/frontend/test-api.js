// Simple API test
const axios = require('axios');

async function testAPI() {
  try {
    console.log('Testing API connection...');
    
    // Test health endpoint
    const healthResponse = await axios.get('http://localhost:8000/health');
    console.log('Health check:', healthResponse.data);
    
    // Test available endpoints
    const rootResponse = await axios.get('http://localhost:8000/');
    console.log('Available endpoints:', rootResponse.data.endpoints);
    
    // Test career prediction with correct endpoint
    const predictionResponse = await axios.post('http://localhost:8000/predict-career', {
      profile: {
        technical_skills: ['python', 'machine_learning'],
        cgpa: 8.5,
        soft_skills: [],
        certifications: [],
        internships: [],
        projects: []
      }
    });
    
    console.log('Prediction result:', predictionResponse.data);
    console.log('✅ API test successful!');
    
  } catch (error) {
    console.error('❌ API test failed:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
    }
  }
}

testAPI();
