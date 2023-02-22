
import 'bootstrap/dist/css/bootstrap.min.css';
import FileService from '../../service/FileService';
import '../Download/Download.css'
import React from "react"; 

export default function Download() {
    const downloadFile = () => {
       FileService.get_file()
    }

    return (
        <div>
          <button className="btn btn-outline-dark" onClick={downloadFile}>Download Results</button>
        </div>
    )
};