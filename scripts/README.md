# Deploy

#### To prod
- bash scripts/deploy.sh

#### To dev:
- bash scripts/deploy.sh dev

#### To skip tests
- bash scripts/deploy.sh dev skip

# Run Grunt
- grunt --gruntfile=/Users/gwg/g2e/scripts/gruntfile.js watch

# Run unit tests 
nosetests --exe

# To compile the Firefox add-on
cfx xpi
