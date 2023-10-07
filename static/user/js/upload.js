// loader css after clicking submit
var form = document.getElementById('uploadForm');
const loader = document.querySelector(".loaderMain");

form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission
    loader.style.display = "flex";
    this.submit();

    // var fileInput = document.getElementById('fileInput').files;
    // console.log(fileInput);
    // for(var i =0; i<fileInput.length; i++){
    //     console.log(fileInput[i].name);
    // }
    // var submitForm = true;
    // var ext = /^.+\.([^.]+)$/.exec(file);
    // fileType = String(ext[1]).toLowerCase();
    // console.log(fileType);
    // if (fileType != "csv" && fileType != "xlsx" && fileType != "xls") {
    //     alert("Please ulpoad csv/xlsx/xls file only");
    //     submitForm = false;
    //     if (submitForm == true) {
    //         loader.style.display = "flex";
    //         // this.submit();
    //     }
    //     else {
    //         event.preventDefault();
    //     }
    // }
});