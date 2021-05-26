var slide = document.getElementById("slide");
var backBtn = document.getElementById("backBtn");
var nextBtn = document.getElementById("nextBtn");
var slideimages = new Array(
     "https://images.pexels.com/photos/4267609/pexels-photo-4267609.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",

"https://images.pexels.com/photos/4267611/pexels-photo-4267611.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940","https://images.unsplash.com/photo-1546954661-59033ac9a921?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", "https://images.pexels.com/photos/532001/pexels-photo-532001.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
);
let i=0;
nextBtn.onclick = function(){
    if(i<3){
        slide.src = slideimages[i+1];
        i++;
    }
}

backBtn.onclick = function(){
    if(i>0){
        slide.src = slideimages[i-1];
        i--;
    }
}
