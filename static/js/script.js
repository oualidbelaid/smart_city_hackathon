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
        if(carousel) {
             carousel.style.transform = 'translateX(' + translateValue + ')';
        }

        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === currentSlide);
        });
    }

     if (prevButton && nextButton && slides.length > 0) {
        showSlide(currentSlide);
         prevButton.addEventListener('click', () => {
            showSlide(currentSlide - 1);
        });

        nextButton.addEventListener('click', () => {
            showSlide(currentSlide + 1);
        });

    // Auto-advance the carousel (optional)
    setInterval(() => {
        showSlide(currentSlide + 1);
    }, 5000); // Change slide every 5 seconds
    }

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
        const listingCards = document.querySelectorAll('.listing-card');

        filterGroups.forEach(group => {
            const checkboxes = group.querySelectorAll('input[type="checkbox"]');
             const selects = group.querySelectorAll('select');


             checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                     const activeFilters = getActiveFilters();
                    filterListings(activeFilters);
                });
            });

            selects.forEach(select => {
               select.addEventListener('change', () => {
                    const activeFilters = getActiveFilters();
                   filterListings(activeFilters);
               });
           });
        });

        function getActiveFilters() {
             const activeFilters = {
                stars: [],
                price: [],
                amenities: [],
                facilities: [],
                 features: [],
                accommodation: [],
                capacity : []
            };


             filterGroups.forEach(group => {
                const groupName = group.querySelector('h4')?.textContent.trim() || group.querySelector('h3')?.textContent.trim();
                const checkboxes = group.querySelectorAll('input[type="checkbox"]:checked');
                  const selects = group.querySelectorAll('select');


                    checkboxes.forEach(checkbox => {
                        const filterValue = checkbox.value;
                        switch (groupName) {
                            case 'Star Rating' :
                            case 'Stars':
                                activeFilters.stars.push(parseInt(filterValue));
                                break;
                             case 'Price Range':
                                activeFilters.price.push(filterValue);
                                break;
                             case 'Amenities':
                                activeFilters.amenities.push(filterValue);
                                break;
                             case 'Facilities':
                                activeFilters.facilities.push(filterValue);
                                break;
                            case 'Features':
                                activeFilters.features.push(filterValue);
                                break;
                             case 'Accommodation Type':
                                    activeFilters.accommodation.push(filterValue);
                                    break;

                        }
                    });

                 selects.forEach(select => {

                    const filterValue = select.value;
                       if(groupName === 'Capacity'){
                            activeFilters.capacity.push(filterValue);
                       }
                 })
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
            const cardStars = card.querySelectorAll('.rating .fas.fa-star').length;
            const cardPriceElement = card.querySelector('.price');
            const cardPrice = cardPriceElement ? cardPriceElement.textContent.length : 0;

            let cardAmenities = '';
            let cardFacilities = '';
            let cardFeatures = '';
             let cardAccommodation = '';
             let cardCapacity = '';
            if (cardType === 'hotel') {
                 const cardAmenityElements = card.querySelectorAll('.amenities');
                cardAmenities = cardAmenityElements.length > 0 ? cardAmenityElements[0].textContent.toLowerCase() : '';
            } else if (cardType === 'complex') {
                const cardFacilityElements = card.querySelectorAll('.details');
                   if(cardFacilityElements && cardFacilityElements.length> 0){
                         cardFacilities = Array.from(cardFacilityElements[0].children)
                    .map(el => el.textContent.toLowerCase()).join(' ');
                       }
                 const cardAccommodationElements = card.querySelectorAll('.details');
                 if(cardAccommodationElements && cardAccommodationElements.length>0){
                      cardAccommodation = Array.from(cardAccommodationElements[0].children)
                     .map(el => el.textContent.toLowerCase()).join(' ');
                 }

            } else if (cardType === 'auberge') {
                const cardFeatureElements = card.querySelectorAll('.features');
                const cardAccommodationElements = card.querySelectorAll('.details');
                 if (cardFeatureElements && cardFeatureElements.length> 0)
                {cardFeatures = cardFeatureElements[0].textContent.toLowerCase() }
                   if(cardAccommodationElements && cardAccommodationElements.length>0) {
                          cardAccommodation = Array.from(cardAccommodationElements[0].children)
                         .map(el => el.textContent.toLowerCase()).join(' ');
                       }
                   const capacityElement = card.querySelector('.details')
                   if(capacityElement){
                        cardCapacity = Array.from(capacityElement.children).find(el => el.textContent.toLowerCase().includes('capacity'))?.textContent.match(/(\d+)/)?.[0]  || '';
                   }
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

           const capacityMatch = activeFilters.capacity.length === 0 || activeFilters.capacity.some(capacity => {
             if (capacity === '') return true; // No capacity filter, matches all
             if (capacity === '4+') return parseInt(cardCapacity) >= 4; // For '4+', check if greater or equal to 4
              return parseInt(cardCapacity) === parseInt(capacity);  // Check for specific numbers.
             } );

           switch (cardType) {
              case 'hotel':
                   return starsMatch && priceMatch && amenitiesMatch;
                case 'complex':
                   return starsMatch && priceMatch && facilitiesMatch && accommodationMatch;
                 case 'auberge':
                     return starsMatch && priceMatch && featuresMatch && accommodationMatch && capacityMatch;
                default:
                  return true;
          }
        }
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navUl = document.querySelector('nav ul');

    if(menuToggle){
      menuToggle.addEventListener('click', function() {
          navUl.classList.toggle('active');
      });
    }
});