

Django signals provide a way to allow decoupled applications to get notified when certain actions occur elsewhere in the application. They allow different parts of your application to communicate without the sender or receiver having to know about each other.


# Defining and Connecting Signals


### Step 1: Create a Signal Receiver Function

Create a new file called `signals.py` in the same directory as your models (e.g., in your app folder).

``` python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book

# Define a receiver function to execute when a new book is created
@receiver(post_save, sender=Book)
def notify_new_book(sender, instance, created, **kwargs):
    if created:
        print(f"New Book Created: '{instance.title}' by Author: '{instance.author.authorName}'")
```

Connect the signal to the receiver: You can use either the` @receiver decorator` (recommended) or the `signal.connect() method`.

#### Parameters (passed to the receiver function):

1. sender: The model class that sent the signal.
2. instance: The actual instance of the model being saved.
3. created: A boolean value indicating whether a `new record was created (True)` or an `existing one was updated (False)`.
4. kwargs: Additional keyword arguments.

### Step 2: Register the Signal in apps.py

Update your app's configuration to include this signal so that it gets loaded when your application starts.

``` python
from django.apps import AppConfig

class YourAppConfig(AppConfig):  # Replace `YourAppConfig` with your app's config class name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'  # Replace with your app's name (e.g., 'books')

    def ready(self):
        import your_app_name.signals  # Replace with your app name

```

### Step 3: Update the `__init__.py` to Load the AppConfig

Add the following line in your app's `__init__.py` file:

``` python
default_app_config = 'your_app_name.apps.YourAppConfig'  # Replace with your app config class and name

```

### Step 4: Create a New Book Entry to Test the Signal

Now, whenever a new Book instance is created, you should see the print message indicating the book title and author.


### Test Code for Django Shell

``` cmd
# import models
from your_app_name.models import Author, Book

# Create a new Author
author = Author.objects.create(authorName="John Doe", authorGender="Male")

# Create a new Book
book = Book.objects.create(title="New Django Book", price=50, author=author)

```


### Overall Flow

1. Define the signal receiver using @receiver with post_save.
2. Connect the receiver by importing it in the ready() method of the app's config.
3. Register the custom app config using default_app_config.
4. Test the signal by creating/updating instances of the specified model.