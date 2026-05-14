from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import re

class GoogleMapsScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with proper options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--headless=new')
            
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            raise
    
    def search_veterinarians(self, location: str):
        """Search for real veterinarians on Google Maps"""
        try:
            search_query = f"veterinary clinics in {location}"
            search_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            self.driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='feed']"))
            )
            
            time.sleep(2)
            
            self.scroll_for_more_results()
            
            clinics = self.extract_clinic_data()
            
            return clinics
            
        except TimeoutException:
            return []
        except Exception as e:
            return []
    
    def scroll_for_more_results(self):
        """Scroll down to load more results"""
        try:
            feed_element = self.driver.find_element(By.CSS_SELECTOR, "[role='feed']")
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", feed_element)
            
            scroll_attempts = 0
            max_scrolls = 8
            
            while scroll_attempts < max_scrolls:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed_element)
                scroll_attempts += 1
                time.sleep(2)
                
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", feed_element)
                if new_height == last_height:
                    break
                last_height = new_height
                
        except Exception as e:
            print(f"Error in scroll_for_more_results")
    
    def extract_clinic_data(self):
        """Extract real clinic data from Google Maps results"""
        clinics = []
        
        try:
            # More specific selector for clinic results
            results = self.driver.find_elements(By.CSS_SELECTOR, "[role='feed'] > div > div > div")
                        
            # Process more results - increased from 15 to 30
            for i, result in enumerate(results[:30]):
                try:
                    clinic_data = self.extract_single_clinic(result)
                    if clinic_data and clinic_data.get('name'):
                        clinics.append(clinic_data)
                    else:
                        print(f"no valid data")
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error in extract_clinic_data")
        
        return clinics
    
    def extract_single_clinic(self, result_element):
        """Extract data from a single clinic result"""
        clinic = {}
        
        try:
            # Try multiple approaches to extract name
            name = self.extract_name(result_element)
            if not name:
                return None
            
            clinic['name'] = name
            
            # Extract other data
            clinic['rating'] = self.extract_rating(result_element)
            clinic['reviews'] = self.extract_reviews(result_element)
            clinic['address'] = self.extract_address(result_element)
            clinic['phone'] = self.extract_phone(result_element)
            clinic['hours'] = self.extract_hours(result_element)
            clinic['website'] = self.extract_website(result_element)
            
            return clinic
            
        except Exception as e:
            return None
    
    def extract_name(self, element):
        """Extract clinic name - improved selection"""
        try:
            # Try multiple selectors in order of priority
            selectors = [
                "div[role='heading'] span",
                "div[role='heading']",
                "h3",
                "div.fontHeadlineLarge",
                "div.fontHeadlineMedium",
                "div[class*='fontHeadline']",
                "div[aria-level='3']",
                "button[data-tooltip] div",
                "div[class*='title']"
            ]
            
            for selector in selectors:
                try:
                    name_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for name_elem in name_elements:
                        name = name_elem.text.strip()
                        # More lenient name validation
                        if (name and len(name) > 2 and 
                            not name.isdigit() and 
                            not name.startswith('http') and
                            'google' not in name.lower()):
                            return name
                except:
                    continue
            
            # Fallback: try to get any text that looks like a clinic name
            try:
                all_text = element.text
                lines = all_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if (len(line) > 3 and 
                        not line.isdigit() and 
                        not line.startswith('http') and
                        'google' not in line.lower() and
                        any(word in line.lower() for word in ['vet', 'clinic', 'animal', 'pet', 'hospital', 'عيادة', 'بيطرية'])):
                        return line
            except:
                pass
            
            return None
        except:
            return None
    
    def extract_rating(self, element):
        """Extract rating"""
        try:
            rating_selectors = [
                "[aria-label*='stars']",
                "[class*='rating']",
                "span[aria-label*='.']",
                "div[aria-label*='stars']",
                "span[class*='fontBodyMedium']"
            ]
            
            for selector in rating_selectors:
                try:
                    rating_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for rating_elem in rating_elements:
                        aria_label = rating_elem.get_attribute('aria-label') or rating_elem.text
                        if aria_label:
                            # Look for ratings in different formats
                            match = re.search(r'(\d+\.\d+)', aria_label)
                            if match:
                                return float(match.group(1))
                            # Also try to find just numbers
                            match = re.search(r'(\d+\.?\d?)', aria_label)
                            if match and float(match.group(1)) <= 5:
                                return float(match.group(1))
                except:
                    continue
            
            return "Rating not available"
        except:
            return "Rating not available"
    
    def extract_reviews(self, element):
        """Extract number of reviews"""
        try:
            review_selectors = [
                "span[class*='reviews']",
                "span[aria-label*='reviews']",
                "div[class*='review']",
                "button[aria-label*='reviews']",
                "span[class*='fontBodyMedium']"
            ]
            
            for selector in review_selectors:
                try:
                    review_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for review_elem in review_elements:
                        text = review_elem.text
                        if any(word in text.lower() for word in ['review', 'تقييم', 'مراجعة']):
                            return text
                except:
                    continue
            
            return "Reviews not available"
        except:
            return "Reviews not available"
    
    def extract_address(self, element):
        """Extract address"""
        try:
            address_selectors = [
                "div.fontBodyMedium > span",
                "[class*='address']",
                "[data-item-id*='address']",
                "div[aria-label*='Address']",
                "button[data-item-id*='address']",
                "div[class*='fontBodyMedium']"
            ]
            
            for selector in address_selectors:
                try:
                    address_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for addr_elem in address_elements:
                        text = addr_elem.text.strip()
                        # More lenient address detection
                        if (text and len(text) > 5 and 
                            not text.startswith('http') and
                            not 'review' in text.lower()):
                            return text
                except:
                    continue
            
            # Fallback: look for text that contains common address indicators
            all_text = element.text
            lines = all_text.split('\n')
            for line in lines:
                line = line.strip()
                if (len(line) > 10 and 
                    any(char.isdigit() for char in line) and
                    not any(word in line.lower() for word in ['review', 'rating', 'website', 'http'])):
                    return line
            
            return "Address not available"
        except:
            return "Address not available"
    
    def extract_phone(self, element):
        """Extract phone number"""
        try:
            text = element.text
            # More comprehensive phone pattern matching
            phone_patterns = [
                r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'\d{2,4}[-.\s]?\d{3}[-.\s]?\d{4}',      # International
                r'\d{10,15}',                            # Plain numbers
                r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}'  # With country code
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    # Return the first valid phone number
                    for match in matches:
                        # Clean up the phone number
                        clean_phone = re.sub(r'[^\d+]', '', match)
                        if len(clean_phone) >= 10:
                            return clean_phone
            
            return "Phone not available"
        except:
            return "Phone not available"
    
    def extract_hours(self, element):
        """Extract business hours"""
        try:
            hours_selectors = [
                "[aria-label*='hours']",
                "[class*='hour']",
                "[data-item-id*='hour']",
                "div[aria-label*='Hours']",
                "div[class*='fontBodyMedium']"
            ]
            
            for selector in hours_selectors:
                try:
                    hours_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for hours_elem in hours_elements:
                        hours = hours_elem.get_attribute('aria-label') or hours_elem.text
                        if hours and any(word in hours.lower() for word in ['hour', 'open', 'closed', 'ساعات', 'عمل']):
                            return hours
                except:
                    continue
            
            return "Hours not available"
        except:
            return "Hours not available"
    
    def extract_website(self, element):
        """Extract website"""
        try:
            website_selectors = [
                "[data-item-id*='authority']",
                "[class*='website']",
                "a[href*='http']",
                "button[aria-label*='website']",
                "div[class*='fontBodyMedium'] a"
            ]
            
            for selector in website_selectors:
                try:
                    website_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for website_elem in website_elements:
                        href = website_elem.get_attribute('href')
                        if href and 'http' in href and 'google.com' not in href:
                            return href
                except:
                    continue
            
            return "Website not available"
        except:
            return "Website not available"
    
    def close(self):
        """Close the browser safely"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except Exception as e:
                print(f"Error closing browser: {e}")