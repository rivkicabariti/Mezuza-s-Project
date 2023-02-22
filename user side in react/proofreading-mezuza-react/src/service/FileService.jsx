import axios from "axios";

class FileService {

    get_file() {
        // debugger
        return axios({
            url: 'http://127.0.0.1:5000//download',
            method: 'GET',
            responseType: 'blob',
        }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'results.pdf');
            document.body.appendChild(link);
            console.log(link)
            link.click();
            // window.open(link.click());
        });
    }
}

export default new FileService