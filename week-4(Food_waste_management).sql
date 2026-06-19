create database food_waste_analysis;
use food_waste_analysis;

create table providers(
provider_id int primary key,
name varchar(150),
type varchar(100),
address varchar(200),
city varchar(100),
contact varchar(70)
);


create table receivers(
receiver_id int primary key,
name varchar(150),
type varchar(100),
city varchar(100),
contact varchar(70)
);

create table food_listings(
food_id int primary key ,
food_name varchar(150),
quantity int,
expiry_date date,
provider_id int,
provider_type varchar(100),
location varchar(100),
food_type varchar(50),
meal_type varchar(50),
foreign key (provider_id) references providers(provider_id)
);

create table claims(
claim_id int primary key,
food_id int,
receiver_id int ,
status varchar(50),
timestamp varchar(50),
foreign key(food_id) references food_listings(food_id),
foreign key(receiver_id) references receivers(receiver_id)

);

select * from providers;
select * from receivers;
select * from food_listings;
select * from claims;

#Analysis
#1)Providers by City
select city ,count(*) as total_providers 
from providers 
group by city ;

#2)Receivers by city 
select city ,count(*) as total_receivers
from receivers
group by city;

#3)Most Contributing Provider 
select provider_id , sum(quantity) as total_quantity
from food_listings 
group by provider_id 
order by total_quantity desc 
limit 1;

#4) Most Claimed Food 
select f.food_name , count(c.claim_id) as total_claims
from food_listings f 
join claims c on f.food_id = c.food_id
group by f.food_name order by total_claims desc
limit 1;

#5)Total Food Quantity
select sum(quantity) as total_food_quantity from food_listings;

#6)Top City by food listing
select location , count(*) as total_listings from food_listings
group by location 
order by total_listings desc 
limit 1;

#7)Most Common food type
select food_type , count(*) as common_food_type 
from food_listings group by food_type
order by common_food_type desc
limit 1;

#8)Claims per food item
select f.food_name, count(c.claim_id) as claim_count 
from food_listings f 
join claims c on f.food_id = c.claim_id 
group by f.food_name;

#9) Provider with most succesful claims
select f.provider_id , count(*) as succesful_claims from claims c 
join food_listings f on c.food_id = f.food_id 
where c.status = 'Completed'
group by f.provider_id 
order by succesful_claims desc limit 1;

#10) Claims status %
select status , round(count(*)*100.0/(select count(*) from claims),2) as percentage
from claims group by status ;

#11) Average quantity claimed
select avg(quantity) as avg_quantity from food_listings;

#12) Most claimed meal type
select meal_type , count(c.claim_id) as total_claims from food_listings f 
join claims c on f.food_id = c.food_id 
group by meal_type order by total_claims desc limit 1;

#13) Total donated quantity by provider
select provider_id , sum(quantity) as total_donated
from food_listings group by provider_id ;

#14) Claim status distribution 
select status , count(*) as total_claims from claims 
group by status;

#15) Top Receiver 
select receiver_id , count(*) as total_claims 
from claims 
group by receiver_id  order by total_claims desc 
limit 1;

#creating view
create view food_summary as
select f.food_id , f.food_name, f.food_type , f.meal_type,f.quantity,f.expiry_date,
p.provider_id , p.name as provider_name ,p.city,p.type as provider_type,replace(replace(replace(
replace(p.contact,'(',' '),')', ''),'.','-'),'x','-') as contact,
coalesce(c.claim_id,0) as claim_id,
coalesce(c.status,'Not Claimed') as status
from food_listings f 
inner join providers p on f.provider_id = p.provider_id
left join( select claim_id , food_id,status from claims)c on f.food_id = c.food_id
order by food_id;



