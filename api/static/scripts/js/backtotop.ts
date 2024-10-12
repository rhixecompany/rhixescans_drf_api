// Get the button
const myCustomButton = document.getElementById('btn-to-top') as HTMLBodyElement;

// When the user scrolls down 20px from the top of the document, show the button
const myScrollFunction = (): void => {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    myCustomButton.classList.add('style_visible');
  } else {
    myCustomButton.classList.remove('style_visible');
  }
};

const mybackToTop = (): void => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// When the user clicks on the button, scroll to the top of the document
myCustomButton.addEventListener('click', mybackToTop);

window.addEventListener('scroll', myScrollFunction);