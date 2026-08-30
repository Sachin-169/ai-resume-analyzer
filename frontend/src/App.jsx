import {useState} from "react";

function App(){
  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeText, setResumeText] = useState("");

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
    setResumeText(data.text);

    console.log(data);
  }

  return(
    <>
      <h1>CareerIQ</h1>
      <h2>AI Resume Analyzer & Career Assistant</h2>
      <input type="file" onChange={(event) => {
          setSelectedFile(event.target.files[0]);
        }}
      />

      <br/><br/>

      <button onClick={uploadResume}>Upload Resume</button>
      <p>Selected File: {" "} {selectedFile ? selectedFile.name : "None"}</p>
      <h2>Extracted Resume</h2>
      <pre>{resumeText}</pre>
    </>
  );
}
export default App;