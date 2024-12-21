document.addEventListener('DOMContentLoaded', function() {
    // Carousel Functionality
    const carousel = document.querySelector('.carousel');
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    let currentSlide = 0;
    
    function showSlide(index) {
        if (index < 0) {
            currentSlide = slides.length - 1;
        } else if (index >= slides.length) {
            currentSlide = 0;
        } else {
            currentSlide = index;
        }
    
        const translateValue = -currentSlide * 100 + '%';
        carousel.style.transform = 'translateX(' + translateValue + ')';
    
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === currentSlide);
        });
    }
    if (prevButton && nextButton) {
        prevButton.addEventListener('click', () => {
            showSlide(currentSlide - 1);
        });
    
        nextButton.addEventListener('click', () => {
            showSlide(currentSlide + 1);
        });
    }
    
    // Auto-advance the carousel (optional)
    setInterval(() => {
        showSlide(currentSlide + 1);
    }, 5000); // Change slide every 5 seconds
    
    // Tab Functionality
    const tabs = document.querySelectorAll('.tab');
    const contentSections = document.querySelectorAll('.content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.target;
    
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
    
            contentSections.forEach(content => {
                content.classList.remove('active');
                if (content.id === target) {
                    content.classList.add('active');
                }
            });
        });
    });
    
        const filterGroups = document.querySelectorAll('.filter-group');
        const listingCards = document.querySelectorAll('.hotel-card, .complex-card, .auberge-card');
    
        filterGroups.forEach(group => {
            const checkboxes = group.querySelectorAll('input[type="checkbox"]');
    
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    const activeFilters = getActiveFilters();
                    filterListings(activeFilters);
                });
            });
        });
    
        function getActiveFilters() {
            const activeFilters = {
                stars: [],
                price: [],
                amenities: [], // For Hotels
                facilities: [], // For Complexe Touristique
                features: [], // For Auberges
                accommodation: [] // For Complexe Touristique and Auberges
            };
    
            filterGroups.forEach(group => {
                const groupName = group.querySelector('h4').textContent.trim();
                const checkboxes = group.querySelectorAll('input[type="checkbox"]:checked');
    
                checkboxes.forEach(checkbox => {
                    const filterValue = checkbox.value;
                    switch (groupName) {
                        case 'Star Rating':
                            activeFilters.stars.push(parseInt(filterValue));
                            break;
                        case 'Price Range':
                            activeFilters.price.push(filterValue);
                            break;
                        case 'Amenities': // For Hotels
                            activeFilters.amenities.push(filterValue);
                            break;
                        case 'Facilities': // For Complexes
                            activeFilters.facilities.push(filterValue);
                            break;
                        case 'Features': // For Auberges
                            activeFilters.features.push(filterValue);
                            break;
                        case 'Accommodation Type': // For Complexes and Auberges
                            activeFilters.accommodation.push(filterValue);
                            break;
                    }
                });
            });
    
            return activeFilters;
        }
    
        function filterListings(activeFilters) {
            listingCards.forEach(card => {
                const cardType = getCardType(card);
                const matchesFilters = doesCardMatchFilters(card, activeFilters, cardType);
                card.style.display = matchesFilters ? 'flex' : 'none';
            });
        }
    
        function getCardType(card) {
            if (card.classList.contains('hotel-card')) {
                return 'hotel';
            } else if (card.classList.contains('complex-card')) {
                return 'complex';
            } else if (card.classList.contains('auberge-card')) {
                return 'auberge';
            }
            return null;
        }
    
        function doesCardMatchFilters(card, activeFilters, cardType) {
            const cardStars = card.querySelectorAll('.stars span').length;
            const cardPriceElement = card.querySelector('.price');
            const cardPrice = cardPriceElement ? cardPriceElement.textContent.length : 0;
    
            // Extract data based on card type
            let cardAmenities = '';
            let cardFacilities = '';
            let cardFeatures = '';
            let cardAccommodation = '';
    
            if (cardType === 'hotel') {
                const cardAmenityElements = card.querySelectorAll('.amenities');
                cardAmenities = cardAmenityElements.length > 0 ? cardAmenityElements[0].textContent.toLowerCase() : '';
            } else if (cardType === 'complex') {
                const cardFacilityElements = card.querySelectorAll('.facilities');
                const cardAccommodationElements = card.querySelectorAll('.accommodation-types');
                cardFacilities = cardFacilityElements.length > 0 ? cardFacilityElements[0].textContent.toLowerCase() : '';
                cardAccommodation = cardAccommodationElements.length > 0 ? cardAccommodationElements[0].textContent.toLowerCase() : '';
            } else if (cardType === 'auberge') {
                const cardFeatureElements = card.querySelectorAll('.features');
                const cardAccommodationElements = card.querySelectorAll('.accommodation-types');
                cardFeatures = cardFeatureElements.length > 0 ? cardFeatureElements[0].textContent.toLowerCase() : '';
                cardAccommodation = cardAccommodationElements.length > 0 ? cardAccommodationElements[0].textContent.toLowerCase() : '';
            }
    
            const starsMatch = activeFilters.stars.length === 0 || activeFilters.stars.includes(cardStars);
            const priceMatch = activeFilters.price.length === 0 || activeFilters.price.some(priceCategory => {
                if (priceCategory === 'budget') return cardPrice === 1;
                if (priceCategory === 'mid-range') return cardPrice === 2;
                if (priceCategory === 'luxury') return cardPrice >= 3;
                return false;
            });
    
            const amenitiesMatch = activeFilters.amenities.length === 0 || activeFilters.amenities.every(amenity => cardAmenities.includes(amenity));
            const facilitiesMatch = activeFilters.facilities.length === 0 || activeFilters.facilities.every(facility => cardFacilities.includes(facility));
            const featuresMatch = activeFilters.features.length === 0 || activeFilters.features.every(feature => cardFeatures.includes(feature));
            const accommodationMatch = activeFilters.accommodation.length === 0 || activeFilters.accommodation.some(accType => cardAccommodation.includes(accType));
    
            // Filter based on card type
            switch (cardType) {
                case 'hotel':
                    return starsMatch && priceMatch && amenitiesMatch;
                case 'complex':
                    return starsMatch && priceMatch && facilitiesMatch && accommodationMatch;
                case 'auberge':
                    return starsMatch && priceMatch && featuresMatch && accommodationMatch;
                default:
                    return true;
            }
        }
    });