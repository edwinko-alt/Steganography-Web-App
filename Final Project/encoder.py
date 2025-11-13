from bakery import assert_equal
from PIL import Image as PIL_Image
import tkinter as tk
import os

def get_message(characters: int) -> str:
    message = input("Please enter your secret message. \n")

    while len(message) > characters:
        message = input("The message can only be " + str(characters) + " long!")

    return message

def prepend_header(message: str) -> str:
    """
    Consumes a message and returns the header of the message
    
    Args:
        message (str): An ASCII message to be encoded
    
    Returns:
        str: The header of the message
    """

    if not message:
        return '000'
    
    #returns a three digit integer
    return format(len(message), '03d') + message

def message_to_binary(message: str) -> str:
    """
    Consumes a message of ASCII characters and returns the binary 
    representation of the characters
    
    Args:
        message (str): A message of ASCII characters
        
    Returns:
        str: The binary value of the message
    """
    
    binary = ''

    for char in message:
        #Format with the parameter '08b' returns the ordinal value as a binary string with 8 digits
        binary = binary + format(ord(char), '08b')

    return binary

def new_color_value(intensity: int, hidden_bit: str) -> int:
    """
    Consumes two values: an integer representing the original Base 10 color intensity value 
    and a string containing the single bit that is to be hidden. It returns a new intensity
    value based on which kind of bit is to be hidden (an even or odd bit)
    
    Args:
        intensity (int): An integer representing the color intensity
        hidden_bit (str): Either a 0 or 1
        
    Returns:
        int: A new intensity value based on the hidden bit"""
    
    if hidden_bit == '1':
        if intensity % 2 == 0:
            intensity += 1
            return intensity
        return intensity
    
    if intensity % 2 == 0:
        return intensity
    return intensity - 1

def hide_bits(image: PIL_Image, binary: str) -> PIL_Image:
    """
    Consumes a Pillow Image and the binary string containing the bits that should be hidden in the 
    image and returns a Pillow Image with the hidden message.
    
    Args:
        image (PIL_Image): A Pillow image
        binary (str): The binary representation of the message to be encoded
        
    Returns:
        PIL_Image: A new Pillow image with the hidden bits encoded
    """

    width, length = image.size
    current_bit = 0

    for w in range(width):
        for l in range(length):
            red, green,blue = image.getpixel((w,l))
            #Checks if the current bit isn't going over the length of the message
            if (current_bit < len(binary)):
                image.putpixel((w,l), (red, new_color_value(green, binary[current_bit]), blue))
            current_bit += 1

    return image



def encode_message(max_chars: int, file: PIL_Image) -> str:
    '''
    main function for hiding a message in an image file
    Args:
        max_chars (int) -> represents the maximum number of characters allowed to be hidden
    Return:
        str: name of the new file where the message is hidden
    '''    
    
    image = PIL_Image.open(file).convert('RGB')  # get RGB Pillow Image format of the image file
 
    # after you have defined:
    #      get_message, prepend_header, message_to_binary   
   
    users_message = get_message(max_chars)  # lets the user enter a message 
    
    message_with_header = prepend_header(users_message)  #prepends the header to the users message
     
    binary_string = message_to_binary(message_with_header)  # convert the full message to a binary string    
   
    # after you have defined:
    #      hide_bits, new_color_value
       
    image = hide_bits(image, binary_string) # encode the message into the image
   
    # save the updated image with a new file name
    new_file_name = "1_" + image # format of 1 + old filename (1 represents green channel)  
    image.save(new_file_name, "PNG") 
      
    return new_file_name
