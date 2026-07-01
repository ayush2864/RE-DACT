import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8001/upload",
        formData
      );

      setResult(response.data);
    } catch (err) {
      console.log(err);
      alert("Upload Failed");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>RE-DACT</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button onClick={uploadFile}>
        Upload
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Detected PII</h2>

          <pre>
            {JSON.stringify(result.entities, null, 2)}
          </pre>

          <a
            href={`http://localhost:8001/download/${result.redacted_pdf.split("\\").pop()}`}
            target="_blank"
            rel="noreferrer"
          >
            <button>Download Redacted PDF</button>
          </a>
        </div>
      )}
    </div>
  );
}

export default App;