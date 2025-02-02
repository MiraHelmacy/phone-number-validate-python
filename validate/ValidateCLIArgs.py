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


class CliArgs:
  #list of phone numbers
  phoneNumbers: list = []
  
  #only valid items
  onlyValid: bool = False
  
  #only invalid items
  onlyInvalid: bool = False
  
  # short option
  short: bool = False

  def __init__(self, config: dict):
    #grab all of the items from the config
    self.phoneNumbers = config['phoneNumbers'] if 'phoneNumbers' in config else self.phoneNumbers
    self.onlyInvalid = config['invalidonly'] if 'invalidonly' in config else self.onlyInvalid
    self.onlyValid = config['validonly'] if 'validonly' in config else self.onlyValid
    self.short = config['short'] if 'short' in config else self.short

  #convert list of phone numbers to a list of PhoneNumberValidate requests that can be passed into pinpoint PhoneNumberValidate
  def PhoneNumberValidateRequests(self) -> list:
    return [{'PhoneNumber': phoneNumber} for phoneNumber in self.phoneNumbers]
  
  #validate the cli args
  def validate(self):
    #no phone numbers if false
    phoneNumbersValid = len(self.phoneNumbers) > 0

    if not phoneNumbersValid:
      return False, "No Phone Numbers"

    #No items to report if false
    itemsToReport = not (self.onlyValid & self.onlyInvalid)
    if not itemsToReport:
      return False, "No items to report"
    
    return True, None
  
  #create a validateResultConfig
  def validateResultConfig(self):
    #config dict
    cfg = {}

    #set invalidonly
    cfg['invalidonly'] = self.onlyInvalid
    
    #set validonly
    cfg['validonly'] = self.onlyValid
    
    #set short
    cfg['short'] = self.short
    
    return cfg