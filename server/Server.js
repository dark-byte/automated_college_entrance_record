const express = require('express');
const multer = require('multer');
const { PythonShell } = require('python-shell');

const app = express();
const port = 3000;

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.post('/predict_license_plate', upload.single('image'), (req, res) => {
  const scriptPath = '/Users/adrish_mitra/Documents/CODE/automated_college_entrance_record/server/predictWithOCR.py'; // Adjust the path
  const imageBuffer = req.file.buffer;

  const options = {
    args: ['--img', 'input_image.jpg'], // Adjust arguments as needed
    scriptPath: scriptPath,
  };

  PythonShell.run(scriptPath, options, (err, results) => {
    if (err) {
      console.error('Error:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      const licensePlate = results[0].trim(); // Adjust result processing
      res.json({ license_plate: licensePlate });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
