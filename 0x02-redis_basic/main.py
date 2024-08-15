#!/usr/bin/env python3

from web import get_page

def main():
    url = "https://mwihoti-portfolio.vercel.app/"
    
    # First access (should fetch from the web and cache it)
    print(get_page(url))
    
    # Second access (should fetch from the cache)
    print(get_page(url))
    
    # Sleep for 10 seconds to let the cache expire (use time.sleep(10) if needed)
    # time.sleep(10)
    
    # Third access (should fetch from the web again)
    print(get_page(url))

if __name__ == "__main__":
    main()
