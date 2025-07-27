async function uploadFile() {
  const file = document.getElementById("fileInput").files[0];
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("output").innerText =
    "Topper: " + data.topper + "\nAverage Marks: " + data.average;
}
