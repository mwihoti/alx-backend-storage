from web import get_page, redis_store  # Importing from the same folder

def main():
    """Main function to test get_page."""
    url = "http://slowwly.robertomurray.co.uk/delay/2000/url/http://www.example.com"
    
    print("First access (should fetch from the web):")
    print(get_page(url))
    
    print("\nSecond access (should fetch from cache):")
    print(get_page(url))
    
    # Wait for the cache to expire
    print("\nWaiting for cache to expire...")
    time.sleep(10)
    
    print("\nThird access (should fetch from the web again):")
    print(get_page(url))
    
    # Display the access count
    count = redis_store.get(f"count:{url}")
    print(f"\nURL was accessed {int(count)} times.")

if __name__ == "__main__":
    main()
