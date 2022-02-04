const file = document.getElementById('FileUploaded');
const submitInput = document.getElementById('submitInput');

file.addEventListener('change', function() {
  let filename = file.files[0].name;
  document.getElementById('FileField').innerHTML =  `Archivo subido`;
  document.getElementById('labelFileUploaded').innerHTML = `Archivo subido - ${filename}`
  document.getElementById('FileField').style.backgroundColor = 'rgba(83, 206, 194, 0.733)';
});

submitInput.addEventListener('click', function() {
  document.getElementById('content-loader').style.display = 'flex';
  document.getElementById('loader').style.display = 'block';
});