$(document).ready(function() {
  // Calculate total price when form is valid and on input change
  var form = $('form');
  var totalPriceElement = $('#total_price');

  function calculateTotalPrice() {
    if (form[0].checkValidity()) {
      var economyTickets = $('#economy_tickets').val() || 0;
      var firstClassTickets = $('#first_class_tickets').val() || 0;
      var premiumEconomyTickets = $('#premium_economy_tickets').val() || 0;

      var pricePerEconomyTicket = 100;
      var pricePerFirstClassTicket = 300;
      var pricePerPremiumEconomyTicket = 200;

      var totalPrice = (economyTickets * pricePerEconomyTicket) + (firstClassTickets * pricePerFirstClassTicket) + (premiumEconomyTickets * pricePerPremiumEconomyTicket);

      var totalNumTickets = parseInt(economyTickets) + parseInt(firstClassTickets) + parseInt(premiumEconomyTickets);
      if (totalNumTickets > 5) {
        totalPrice *= 0.8;
      }

      totalPriceElement.html("$" + totalPrice.toFixed(2));
    }
  }

  form.on('input', calculateTotalPrice);
  form.on('submit', calculateTotalPrice);
});