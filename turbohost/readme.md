Smokin Goldshop
=======================

This project was one that I worked on for a few years as the sole development contractor. I built this from the ground up as an administration panel for an ecommerce site that sold exclusively RuneScape "Gold Pieces" as a real-money-trade website. 

This site was built to run on Google App Engine with Python v2.7 and the built-in version of Django.  

The administration site featured deep integration with Paypal's NVP API. This integration began with an endpoint that allowed the users to modify product pricing in the administration panel to update live on a php powered site. This allowed the site to verify that the products were being sold for the correct prices. 

Paypal would then send order notifications to an endpoint located in the admin panel to add the customer order to the system. The system would then check various factors about the order for fraud checking, including matching the IP Address with the order shipping information from paypal, and verifying that information based on what the customer was able to tell the delivery agent. 

The system allowed for searching of orders that were stored in the system, grouping of orders by customer, tracking of commission from sales, tracking of referrals, tracking of delivery agent payments, and automated paypal refunds without needing to log into Paypal directly. 