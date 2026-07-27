import {useState} from "react";

function App(){
  const [selectedFile, setSelectedFile] = useState(null);
  async function uploadResume(){
    if (!selectedFile) {
      alert("Please select a resume first.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", selectedFile);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method:"POST",
      body:formData,
    });

    const data = await response.json();
    console.log(data);
  }

  return(
    <>
      <h1>AI Resume Analyzer</h1>
      <input type="file" onChange={(event) => {
          setSelectedFile(event.target.files[0]);
        }}
      />

      <br/><br/>

      <button onClick={uploadResume}>Upload Resume</button>
      <p>Selected File: {" "} {selectedFile ? selectedFile.name : "None"}</p>
    </>
  );
}
export default App;