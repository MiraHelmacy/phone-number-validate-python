"""
The MIT License (MIT)

Copyright © 2025 Alex Helmacy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from json import JSONEncoder

def awsCliCommand(phoneNumber: str) -> str:
  return f"aws pinpoint phone-number-validate --number-validate-request PhoneNumber={phoneNumber}"

class ValidateResult:
  #result dict
  result: dict
  
  #short option
  short: bool = False
  
  #onlyinvalid option
  onlyInvalid: bool = False

  #onlyvalid option
  onlyValid: bool = False

  def __init__(self, config: dict):
    #extract items from the config
    self.short = config['short'] if 'short' in config else self.short
    self.onlyInvalid = config['invalidonly'] if 'invalidonly' in config else self.onlyInvalid
    self.onlyValid = config['validonly'] if 'validonly' in config else self.onlyValid
    
    #validate input
    if self.onlyValid & self.onlyInvalid:
      raise ValueError("Invalid Config. Both Only Invalid and Only Valid Selected")
    
    #create resulr
    self.result = {
      'valid': [],
      'invalid': []
    }
    
  def Add(self, validateResponse: dict):
    #determine aws cli command
    AwsCliCommand = awsCliCommand(validateResponse['OriginalPhoneNumber'])
    
    #create a new item
    item = {
      'AwsCliCommand': AwsCliCommand,
      'NumberValidateResponse': validateResponse
    }
    
    #check if phone number is valid and add to appropriate list in the result
    if validateResponse['PhoneType'] == "INVALID":
      self.result['invalid'].append(item)
    else:
      self.result['valid'].append(item)

#Validate Result JSON Encoder
class ValidateResultEncoder(JSONEncoder):
  def default(self, o):
    #check if o is a ValidateResult object
    if type(o) == ValidateResult:
      
      #set valid and invalid result
      valid = o.result['valid']
      invalid = o.result['invalid']
      
      #if short option requested set valid and invalid short result
      if o.short:
        valid = [{'AwsCliCommand': item['AwsCliCommand'], 'PhoneNumber': item['NumberValidateResponse']['OriginalPhoneNumber']} for item in valid]
        invalid = [{'AwsCliCommand': item['AwsCliCommand'], 'PhoneNumber': item['NumberValidateResponse']['OriginalPhoneNumber']} for item in invalid]
      
      #match the combinations of onlyvalid and onlyinvalid
      match o.onlyValid, o.onlyInvalid:
        #only valid case
        case True, False:
          return {
            'Valid': valid 
          }
        #only invalid case
        case False, True:
          return {
            'Invalid': invalid
          }
        #standard option
        case False, False:
          return {
            'Valid': valid,
            'Invalid': invalid
          }
        #invalid config
        case True, True:
          raise ValueError("Invalid ValidateResult Configuration. Both Invalid Only and Valid Only selected.")
      
    #o is not a ValidateResult object
    return super().default(o)