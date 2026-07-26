import {useState} from "react";

function App(){
  const [selectedFile, setSelectedFile] = useState(null);
  return(
    <>
      <h1>AI Resume Analyzer</h1>
      <input type="file" onChange={(event) => {
          setSelectedFile(event.target.files[0]);
        }}
      />

      <p>
        Selected File: {" "} {selectedFile ? selectedFile.name : "None"}
      </p>
    </>
  );
}
export default App;