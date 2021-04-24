import getFHIRIGs
import validate
import analytics

if __name__ == '__main__':
    print('Downloading packages')
    getFHIRIGs.getPackages()
    
    print('Validating packages')
    validate.validatePackages()
    
    print('Performing analytics')
    analytics.analizePackages()