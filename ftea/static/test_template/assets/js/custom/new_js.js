const taskFrame = document.getElementsByClassName('task-frame');
// const taseInn = document.getElementById('getTaskIn');
const keyInn = document.getElementById('Key');
const titleInn = document.getElementById('Title');
const statusInn = document.getElementById('Status');
const contentInn = document.getElementById('Content');
const createdInn = document.getElementById('Created');
const creatorInn = document.getElementById('Creator');

for (i=0; i<taskFrame.length; i++) {
    taskFrame[i].addEventListener("click", function () {
        let taskData = [];
        let taskKey = this.childNodes[1].childNodes[1].innerHTML;
        let taskTitle = this.childNodes[1].childNodes[4].innerHTML;
        let taskStatus = this.childNodes[3].childNodes[4].innerHTML;
        let taskContent = this.childNodes[3].childNodes[6].innerHTML;
        let taskCreated = this.childNodes[3].childNodes[8].innerHTML;
        let taskCreator = this.childNodes[3].childNodes[10].innerHTML;
        console.log(this.childNodes[3].childNodes);
        taskData.push(taskKey, taskTitle, taskStatus, taskContent, taskCreated.slice(0, 10), taskCreator);
        createElementToDisplay(taskData);
        for (j=0; j<taskFrame.length; j++) {
            taskFrame[j].classList.remove('mystyle');
        }
        this.classList.add("mystyle");
    })
}

function createElementToDisplay(aj){
    keyInn.innerHTML = '';
    statusInn.innerHTML = '';
    titleInn.innerHTML = '';
    contentInn.innerHTML = '';
    keyInn.innerHTML = aj[0];
    statusInn.innerHTML = aj[2];
    titleInn.innerHTML = aj[1];
    contentInn.innerHTML = aj[3];
    createdInn.innerHTML = aj[4];
    creatorInn.innerHTML = aj[5];
}

        // if ('mystyle' in this.classList) {
        //     this.classList.remove("mystyle");
        // } else {
        //     this.classList.add("mystyle");
        // }
        // // this.classList.toggle("mystyle");