# Nahasapeemapetilon  
## Rubin Peci, Adil Gondal, Amit Narang, and Qian Zhou    
   
### CryptUwU :tongue: :eyes:   
   
A cryptocurrency forum and market tool!   
   
#### Features 
- Allows users to make accounts, login, and make posts 
- Posts can be upvoted, saved, and replied to. 
- Stats regarding various crytocurrencies can be viewed, and some coins can be favorited 
 
#### How to run the project   
1. Create a virtual environment  
`python -m venv test/`  
   
2. Clone the repo       
`git clone https://github.com/adil11111/SDFP`   
    
3. Activate your virtual environment   
`source test/bin/activate`    
    
4. Install the necessary python modules   
`pip install -r requirements.txt`   
   
5. Procure API keys for the Nomics and Plotly APIs  
   
Nomics:  
Get your free API key [here](https://p.nomics.com/cryptocurrency-bitcoin-api)   
Follow the instructions provided, and your API key will be emailed to you   
Put that API key in the `keys/nomics.json` file, replace the empty string for the entry "API"   
   
Plotly:   
   
Make an account [here](https://plot.ly/Auth/login/?next=%2Fsettings) and procure your API key 
Replace the empty string for "username" and "API" with your information. 
 
6. Once the above steps are completed, run the follow command at the root of the repo   
`flask run`     
*If any errors arise, verify you completed the above steps, and try again. If the error still persists, feel free to open an issue in our repo!*    
    
7. Open your browser, and connect to this [link](localhost:5000)   
The link points to localhost:5000, which is the server on which the program is running on your computer   
    
8. Use the site! Make an account, test things out, do as you please.    
   
If you encounter any issues worth noting, open an issue so we can get to it!   
   
Hope you enjoy :blush:  
