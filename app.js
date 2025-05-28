const express = require('express');
const redis = require('redis');
const axios = require('axios');

const app = express();
app.use(express.json());

const redisClient = redis.createClient();
redisClient.connect().catch(console.error);

const SENSOR_CACHE_KEY = 'sensor-data';

app.get('/sensor-data', async (req, res) => {
  try {
    const cachedData = await redisClient.get(SENSOR_CACHE_KEY);
    if (cachedData) {
      console.log('Dados do Redis');
      return res.json(JSON.parse(cachedData));
    }

    const sensorData = {
      temperature: (20 + Math.random() * 15).toFixed(2), 
      pressure: (100 + Math.random() * 50).toFixed(2)    
    };

    await redisClient.setEx(SENSOR_CACHE_KEY, 10, JSON.stringify(sensorData));

    console.log('Dados gerados');
    res.json(sensorData);

  } catch (error) {
    res.status(500).send('Erro no servidor');
  }
});

app.post('/alert', async (req, res) => {
  try {
    const alertData = req.body;

    await axios.post('http://localhost:5000/event', alertData);

    res.send('Alerta enviado para API Python');
  } catch (error) {
    res.status(500).send('Erro ao enviar alerta');
  }
});

app.listen(3000, () => {
  console.log('API Node.js rodando na porta 3000');
});
