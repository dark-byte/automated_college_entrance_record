const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(express.json({ limit: '10mb' })); // Increase the payload size limit if needed

app.post('/extractText', (req, res) => {
  // Assuming the image is sent in the request body as { image: 'base64encodeddata' }
  const imageData = req.body.image;

  // Save the image data to a temporary file
  const tempImagePath = path.join(__dirname, 'temp_image.jpg');
  fs.writeFileSync(tempImagePath, imageData, 'base64');

  const pythonScript = path.join(__dirname, 'text_extraction_module.py');
  const pythonProcess = spawn('python', [pythonScript, tempImagePath]);

  pythonProcess.stdout.on('data', (data) => {
    const result = JSON.parse(data.toString());
    
    // Remove the temporary image file
    fs.unlinkSync(tempImagePath);

    res.json(result);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
    
    // Remove the temporary image file
    fs.unlinkSync(tempImagePath);

    res.status(500).send('Internal Server Error');
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
