import React, { useState } from "react";
import ImageUploader from "react-images-upload";
import axios from "axios"
import "./Upload.css"
import Download from '../Download/Download';
import FileService from '../../service/FileService';
//import Progress from "../Progress/Progress";
import 'bootstrap/dist/css/bootstrap.min.css';

export default function UploadComponent(props) {

  const [file, setFile] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});
  const [SuccessfullUploaded, setSuccessfullUploaded] = useState({});
  const [Result, setResult] = useState({});
  const [Progress, setProgress] = useState({});
  const [Upload, setUpload] = useState({});
  const [showUpload, setShowUpload] = useState(true);
  const [showConfirm, setShowConfirm] = useState(false);
  const [showResult, setShowResult] = useState(false)

  const onDrop = (pictureFiles, pictureDataURLs) => {
    setShowConfirm(true);
    setFile(file.concat(pictureFiles))
    const newImagesUploaded = pictureDataURLs.slice(
      props.defaultImages.length
    );
    console.warn("pictureDataURLs =>", newImagesUploaded);
    props.handleChange(newImagesUploaded);
  };

  const upload_file = () => {
    setShowUpload(false);
    const formData = new FormData();
    // file.map((a,i)=>formData.append(`${i}`,a))

    formData.append('image', file[0]);
    console.log(formData)
    axios.post('http://127.0.0.1:5000/upload-file', formData, {

      onUploadProgress: (progressEvent) => {
        //how much time need finish
        if (progressEvent.lengthComputable) {
          const copy = { ...uploadProgress };
          copy[file[0].name] = {
            state: "pending",
            percentage: (progressEvent.loaded / progressEvent.total) * 100
          };
          setUploadProgress(copy);
        }
      },
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(response => {
        const copy = { ...uploadProgress };
        copy[file[0].name] = { state: "done", percentage: 100 };
        setUploadProgress(copy);
        setSuccessfullUploaded(true)
        setShowResult(true)
        setResult(response.data)
        console.log("helo")
        console.log(response.data)
        return true;
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
          const copy = { ...uploadProgress };
          copy[file[0].name] = { state: "error", percentage: 0 };
          setUpload(true)
          Progress(copy)
          return false;
        }
      })
  }

  const downloadFile = () => {
    FileService.get_file()
  }




  return (
    <div>
      {
        showUpload ?
          <div className="upload">
            <ImageUploader className="fileUploader c"
              withIcon={true}
              withLabel={false}
              withPreview={true}
              buttonText={"Add a Mezuzah"}
              fileSizeError={"File size is too big!"}
              fileTypeError={"This extension is not supported!"}
              onChange={onDrop}
              imgExtension={props.imgExtension}
              maxFileSize={props.maxFileSize}
              buttonClassName='fileContainer chooseFileButton'
            />
            {showConfirm ?
              <div className="confirm">
                <button type="button" class="btn btn-outline-dark" onClick={upload_file}>Confirm upload</button>
              </div> : ''
            }
          </div> :
          <div>{showResult?
            <div>
              <br></br>
              <iframe className="pdf-file" src={Result}></iframe>
              {/* <button className="btn btn-outline-dark" onClick={downloadFile}>Download Results</button> */}
            </div>:<div><br></br><br></br><h3 className="waiting">waiting to results...</h3></div>
}
          </div>

      }

    </div>
  )

}
