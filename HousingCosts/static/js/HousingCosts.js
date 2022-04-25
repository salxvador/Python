// This function displays the first image in the slideshow when the page loads
var slideIndex = 1;
showSlides(slideIndex);

// This function changes the slide when the left or right arrows are clicked
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// This function changes the slide when the dots are clicked
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var slides = document.getElementsByClassName("slide"); // This takes all slideshow elements and stores them in the variable array
    var dots = document.getElementsByClassName("dot"); // Sore all dots in an array
    if (n > slides.length) {slideIndex = 1}; // this is needed so that the slide numbers will loop around the array
    if (n < 1) {slideIndex = slides.length};
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none"; // This for loop takes each item in the array and sets the display to none (default)
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", ""); // This for loop takes each item in the dots array and removes "active"
    }
    slides[slideIndex - 1].style.display = "block"; // displays the image
    dots[slideIndex - 1].className += " active"; // add the active styling to the dot for the image
}