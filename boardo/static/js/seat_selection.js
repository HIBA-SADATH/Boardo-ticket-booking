document.addEventListener('DOMContentLoaded', function () {
  const seatButtons  = document.querySelectorAll('.seat.available');
  const selectedBox  = document.getElementById('selectedSeats');
  const totalPriceEl = document.getElementById('totalPrice');
  const seatInput    = document.getElementById('seatInput');
  const continueBtn  = document.querySelector('.continue-btn');
  const bookingForm  = document.querySelector('.summary-box form');

  const selectedSeats = new Map(); // seatId -> { number, price }

  function formatMoney(n) {
    return n.toLocaleString('en-IN');
  }

  function renderSummary() {
    selectedBox.innerHTML = '';

    if (selectedSeats.size === 0) {
      selectedBox.classList.remove('has-seats');
      selectedBox.textContent = 'No seat selected';
    } else {
      selectedBox.classList.add('has-seats');
      selectedSeats.forEach((seat, id) => {
        const chip = document.createElement('span');
        chip.className = 'seat-chip';
        chip.innerHTML = `${seat.number} <button type="button" aria-label="Remove seat ${seat.number}" data-id="${id}">&times;</button>`;
        selectedBox.appendChild(chip);
      });
    }

    let total = 0;
    selectedSeats.forEach(seat => total += seat.price);
    totalPriceEl.textContent = formatMoney(total);

    seatInput.value = Array.from(selectedSeats.keys()).join(',');
    console.log("Seat Input:", seatInput.value);
    continueBtn.disabled = selectedSeats.size === 0;

    selectedBox.querySelectorAll('.seat-chip button').forEach(btn => {
      btn.addEventListener('click', () => toggleSeat(btn.dataset.id));
    });
  }

  function toggleSeat(id) {
    const seatBtn = document.querySelector(`.seat.available[data-id="${id}"]`);
    if (!seatBtn) return;

    if (selectedSeats.has(id)) {
      selectedSeats.delete(id);
      seatBtn.classList.remove('selected');
    } else {
      selectedSeats.set(id, {
        number: seatBtn.dataset.number,
        price: parseFloat(seatBtn.dataset.price) || 0
      });
      seatBtn.classList.add('selected');
    }

    renderSummary();
  }

  seatButtons.forEach(btn => {
    btn.addEventListener('click', () => toggleSeat(btn.dataset.id));
  });

  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      if (selectedSeats.size === 0) {
        e.preventDefault();
        alert('Please select at least one seat to continue.');
      }
    });
  }

  continueBtn.disabled = true;
});