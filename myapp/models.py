from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class register(models.Model):
    firstname=models.CharField(max_length=15)
    lastname=models.CharField(max_length=15)
    username=models.CharField(max_length=15,default=None)
    email=models.EmailField()
    psw=models.CharField(max_length=15)
    cpsw=models.CharField(max_length=15)
    # prf_pic = models.ImageField(upload_to='profile_pics')
    
    def __str__(s):
        return f'{s.nm}-{s.em}'

class PasswordReset(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

class addproduct(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pnm=models.CharField(max_length=15)
    athr=models.CharField(max_length=15, default=None)
    CATEGORY_CHOICES = [
        ('Thriller', 'Thriller'),
        ('Mystery', 'Mystery'),
        ('Horror', 'Horror'),
        ('Comics', 'Comics'),
        ('Adventure', 'Adventure'),
        ('Romance', 'Romance'),
        ('Historical fiction', 'Historical fiction'),
        ('Literary fiction', 'Literary fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Autobiography', 'Autobiography'),
        ('Memoir', 'Memoir'),
        ('History', 'History'),
        ('Travel', 'Travel'),
        ('Science', 'Science'),
        ('Philosophy', 'Philosophy'),
        ('Essays', 'Essays'),
        ('Business', 'Business'),
        ('Children\'s Book', 'Children\'s Book'),
        ('Classic Literature', 'Classic Literature'),
        ('Short Stories', 'Short Stories'),
        ('Drama', 'Drama'),
        ('Poetry', 'Poetry'),
        ('Self-help and Motivational', 'Self-help and Motivational')
    ]
    
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Malayalam', 'Malayalam'),
    ]

    cat = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    lang = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    publ = models.CharField(max_length=25)
    isbn = models.IntegerField()
    pr = models.IntegerField() 
    qty = models.IntegerField()
    img = models.ImageField(upload_to='p_images')

    def discounted_price(self):
        return int(self.pr * 0.5)

    
class customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    DISTRICT_CHOICES = (
        ('Alappuzha','Alappuzha'),
        ('Ernakulam','Ernakulam'),
        ('Idukki','Idukki'),
        ('Kannur','Kannur'),
        ('Kasaragod','Kasaragod'),
        ('Kollam','Kollam'),
        ('Kottayam','Kottayam'),
        ('Kozhikode','Kozhikode'),
        ('Malappuram','Malappuram'),
        ('Palakkad','Palakkad'),
        ('Pathanamthitta','Pathanamthitta'),
        ('Thiruvananthapuram','Thiruvananthapuram'),
        ('Thrissur','Thrissur'),
        ('Wayanad','Wayanad'),
    )
    district = models.CharField(choices=DISTRICT_CHOICES,max_length=50)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    STATE_CHOICES = (
        ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
        ('Andhra Pradesh','Andhra Pradesh'),
        ('Arunachal Pradesh','Arunachal Pradesh'),
        ('Assam','Assam'),
        ('Bihar','Bihar'),
        ('Chandigarh','Chandigarh'),
        ('Chhattisgarh','Chhattisgarh'),
        ('Dadra & Nagar Haveli and Daman & Diu','Dadra & Nagar Haveli and Daman & Diu'),
        ('Delhi','Delhi'),
        ('Goa','Goa'),
        ('Gujarat','Gujarat'),
        ('Haryana','Haryana'),
        ('Himachal Pradesh','Himachal Pradesh'),
        ('Jammu & Kashmir','Jammu & Kashmir'),
        ('Jharkhand','Jharkhand'),
        ('Karnataka','Karnataka'),
        ('Kerala','Kerala'),
        ('Ladakh','Ladakh'),
        ('Lakshadweep','Lakshadweep'),
        ('Madhya Pradesh','Madhya Pradesh'),
        ('Maharashtra','Maharashtra'),
        ('Manipur','Manipur'),
        ('Meghalaya','Meghalaya'),
        ('Mizoram','Mizoram'),
        ('Nagaland','Nagaland'),
        ('Odisha','Odisha'),
        ('Puducherry','Puducherry'),
        ('Punjab','Punjab'),
        ('Rajasthan','Rajasthan'),
        ('Sikkim','Sikkim'),
        ('Tamil Nadu','Tamil Nadu'),
        ('Telangana','Telangana'),
        ('Tripura','Tripura'),
        ('Uttar Pradesh','Uttar Pradesh'),
        ('Uttarakhand','Uttarakhand'),
        ('West Bengal','West Bengal'),
        )
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(s):
        return s.name 

class cartpro(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(addproduct,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


STATUS_CHOICES = {
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
}

class payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    buy_now_product_id = models.IntegerField(null=True, blank=True)  


class orderplaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    product = models.ForeignKey(addproduct,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    Payment = models.ForeignKey(payment,on_delete=models.CASCADE,default="")

class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(addproduct,on_delete=models.CASCADE)
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(addproduct,on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)