// You can use this file to fetch and display user data dynamically
// using JavaScript and potentially an API.

// Example of setting data dynamically (replace with your actual data-fetching logic):
document.addEventListener('DOMContentLoaded', function() {
    const firstNameSpan = document.getElementById('first-name');
    const lastNameSpan = document.getElementById('last-name');
    const idNumberSpan = document.getElementById('id-number');
    const sexSpan = document.getElementById('sex');
    const staysSpan = document.getElementById('stays');
    const clientTypeSpan = document.getElementById('client-type');
  
    // Replace with actual data from your user object/database
    const user = {
        firstName: "John",
        lastName: "Doe",
        idNumber: "1234567890",
        sex: "Male",
        numberOfStays: 3,
        clientType: "Individual"
    };
  
    firstNameSpan.textContent = user.firstName;
    lastNameSpan.textContent = user.lastName;
    idNumberSpan.textContent = user.idNumber;
    sexSpan.textContent = user.sex;
    staysSpan.textContent = user.numberOfStays;
    clientTypeSpan.textContent = user.clientType;
  });