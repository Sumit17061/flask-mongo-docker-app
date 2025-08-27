const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send(`
    <form action="/submit" method="post">
      <input name="name" placeholder="Enter your name" />
      <input name="email" placeholder="Enter your email" />
      <button type="submit">Submit</button>
    </form>
  `);
});

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post('http://backend:5000/submit', req.body);
    res.send(response.data);
  } catch (err) {
    res.send('Error: ' + err.message);
  }
});

app.listen(port, () => {
  console.log(`Frontend running on port ${port}`);
});

