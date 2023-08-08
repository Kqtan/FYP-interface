function deleteMessage(messageId) {
    fetch("/view/delete_msg", {
        method: "POST",
        body: JSON.stringify({ messageId: messageId })
    }).then((_res) => {
        window.location.href = "/view";
    })
}

function openMessage(messageId) {
    fetch("/view/msg/" + messageId, {
        method: "POST",
        body: JSON.stringify({ messageId: messageId })
    }).then((_res) => {
        window.location.href = "/view/msg/" + messageId;
    })
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

function showSpinner() {
    var button = document.getElementById('myButton');
    var spinner = document.getElementById('spinner');
    
    button.disabled = true; // Disable the button
    button.innerHTML = ''; // Remove the button text
    
    spinner.style.display = 'inline-block'; // Show the spinner
}

const arrowLink = document.querySelector('.arrow-link');
arrowLink.addEventListener('click', function(e) {
    e.preventDefault();
    const section = document.querySelector(this.getAttribute('href'));
    section.scrollIntoView({ behavior: 'smooth' });
});

$('.back-to-top').click(function() {
    $('html, body').animate({ scrollTop: 0 }, 'slow');
    return false;
});


// for the customer quotes
const quotes = document.querySelectorAll('.quote');
let currentIndex = 0;

function showQuote(index) {
    quotes.forEach((quote, i) => {
        if (i === index) {
            quote.style.display = 'block';
        } else {
            quote.style.display = 'none';
        }
    });
}

document.getElementById('prevBtn').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + quotes.length) % quotes.length;
    showQuote(currentIndex);
});

document.getElementById('nextBtn').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % quotes.length;
    showQuote(currentIndex);
});

showQuote(currentIndex);



showQuote(currentIndex);

// Adjust container scroll behavior
quoteContainer.addEventListener('scroll', () => {
    const scrollPercentage = (quoteContainer.scrollLeft / quoteContainer.scrollWidth) * 100;
    if (scrollPercentage < 20) {
        currentIndex = 0;
    } else if (scrollPercentage > 80) {
        currentIndex = quotes.length - 1;
    } else {
        currentIndex = Math.round((scrollPercentage / 100) * quotes.length);
    }
    showQuote(currentIndex);
});
