function checkSpam() {
    const userInput = document.getElementById('userMessage').value.toLowerCase();
    const resultElement = document.getElementById('result');
  
    // Perform your SMS spam classification here (replace this logic with your classifier)
    // For example, let's assume 'spamWords' contains a list of spam keywords
    const spamWords = ['offer', 'free', 'win', 'prize', 'discount'];
  
    const isSpam = spamWords.some(word => userInput.includes(word));
  
    if (isSpam) {
      resultElement.innerText = 'This message is classified as SPAM.';
      resultElement.style.color = 'red';
    } else {
      resultElement.innerText = 'This message is classified as HAM (not spam).';
      resultElement.style.color = 'green';
    }
  }
  