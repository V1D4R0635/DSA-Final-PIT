import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='0635',
    database='recipes_db'
)
cursor = conn.cursor()

# To add a new recipe to the database
def add_recipe(title, category, instructions, ingredients):
    cursor.execute("INSERT INTO recipes (title, category, instructions) VALUES (%s, %s, %s)", (title, category, instructions))
    recipe_id = cursor.lastrowid
    for ingredient in ingredients:
        cursor.execute("INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)", (recipe_id, ingredient))
    conn.commit()
    messagebox.showinfo("Success", "Recipe added successfully.")

# Deletes a recipe from the database
def delete_recipe(recipe_id):
    cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = %s", (recipe_id,))
    conn.commit()
    messagebox.showinfo("Success", "Recipe deleted successfully.")

# To edit a recipe in the database
def edit_recipe(recipe_id, title, category, instructions, ingredients):
    cursor.execute("UPDATE recipes SET title = %s, category = %s, instructions = %s WHERE id = %s", (title, category, instructions, recipe_id))
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = %s", (recipe_id,))
    for ingredient in ingredients:
        cursor.execute("INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)", (recipe_id, ingredient))
    conn.commit()
    messagebox.showinfo("Success", "Recipe updated successfully.")

# Search for recipes by category
def search_recipe_by_category(category):
    cursor.execute("SELECT * FROM recipes WHERE category = %s", (category,))
    recipes = cursor.fetchall()
    if not recipes:
        messagebox.showinfo("No Recipes", "No recipes found in this category.")
    else:
        recipe_text = ""
        for recipe in recipes:
            recipe_text += f"ID: {recipe[0]}, Title: {recipe[1]}, Category: {recipe[2]}, Instructions:\n{recipe[3]}\nIngredients:\n"
            cursor.execute("SELECT ingredient FROM ingredients WHERE recipe_id = %s", (recipe[0],))
            ingredients = cursor.fetchall()
            for ingredient in ingredients:
                recipe_text += f"{ingredient[0]}\n"
            recipe_text += "\n"  # Add a blank line between recipes
        messagebox.showinfo("Recipes", recipe_text)

# Functions to handle the button clicks
def add_recipe_click():
    title = title_entry.get()
    category = category_entry.get()
    instructions = instructions_text.get("1.0", "end-1c")
    ingredients = ingredients_text.get("1.0", "end-1c").split('\n')
    add_recipe(title, category, instructions, ingredients)

def delete_recipe_click():
    recipe_id = recipe_id_entry.get()
    delete_recipe(recipe_id)

def edit_recipe_click():
    recipe_id = recipe_id_entry_edit.get()
    title = title_entry_edit.get()
    category = category_entry_edit.get()
    instructions = instructions_text_edit.get("1.0", "end-1c")
    ingredients = ingredients_text_edit.get("1.0", "end-1c").split('\n')
    edit_recipe(recipe_id, title, category, instructions, ingredients)

def search_recipe_click():
    category = search_category_entry.get()
    search_recipe_by_category(category)

# Function to show frames
def show_frame(frame):
    frame.tkraise()

# Create main window
root = tk.Tk()
root.title("Recipe Sorter")

# Create frames
main_menu_frame = tk.Frame(root)
add_recipe_frame = tk.Frame(root)
delete_recipe_frame = tk.Frame(root)
edit_recipe_frame = tk.Frame(root)
search_recipe_frame = tk.Frame(root)

for frame in (main_menu_frame, add_recipe_frame, delete_recipe_frame, edit_recipe_frame, search_recipe_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Main Menu
tk.Label(main_menu_frame, text="Main Menu", font=('Helvetica', 18, 'bold')).pack(pady=10)
tk.Button(main_menu_frame, text="Add Recipe", command=lambda: show_frame(add_recipe_frame), bg='green', fg='white').pack(pady=5)
tk.Button(main_menu_frame, text="Delete Recipe", command=lambda: show_frame(delete_recipe_frame), bg='red', fg='white').pack(pady=5)
tk.Button(main_menu_frame, text="Edit Recipe", command=lambda: show_frame(edit_recipe_frame), bg='yellow', fg='black').pack(pady=5)
tk.Button(main_menu_frame, text="Search Recipe", command=lambda: show_frame(search_recipe_frame), bg='teal', fg='white').pack(pady=5)

# Add Recipe Frame
tk.Label(add_recipe_frame, text="Add Recipe", font=('Helvetica', 18, 'bold')).pack(pady=10)
tk.Button(add_recipe_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame), bg='teal', fg='white').pack(pady=5)

tk.Label(add_recipe_frame, text="Title:").pack(anchor='w')
title_entry = tk.Entry(add_recipe_frame)
title_entry.pack(anchor='w')

tk.Label(add_recipe_frame, text="Category:").pack(anchor='w')
category_entry = tk.Entry(add_recipe_frame)
category_entry.pack(anchor='w')

tk.Label(add_recipe_frame, text="Instructions:").pack(anchor='w')
instructions_text = tk.Text(add_recipe_frame, width=40, height=6)
instructions_text.pack(anchor='w')

tk.Label(add_recipe_frame, text="Ingredients:").pack(anchor='w')
ingredients_text = tk.Text(add_recipe_frame, width=40, height=6)
ingredients_text.pack(anchor='w')

tk.Button(add_recipe_frame, text="Add Recipe", command=add_recipe_click, bg='green', fg='white').pack(pady=5)

# Delete Recipe Frame
tk.Label(delete_recipe_frame, text="Delete Recipe", font=('Helvetica', 18, 'bold')).pack(pady=10)
tk.Button(delete_recipe_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame), bg='teal', fg='white').pack(pady=5)

tk.Label(delete_recipe_frame, text="Recipe ID to delete:").pack(anchor='w')
recipe_id_entry = tk.Entry(delete_recipe_frame)
recipe_id_entry.pack(anchor='w')

tk.Button(delete_recipe_frame, text="Delete Recipe", command=delete_recipe_click, bg='red', fg='white').pack(pady=5)

# Edit Recipe Frame
tk.Label(edit_recipe_frame, text="Edit Recipe", font=('Helvetica', 18, 'bold')).pack(pady=10)
tk.Button(edit_recipe_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame), bg='teal', fg='white').pack(pady=5)

tk.Label(edit_recipe_frame, text="Recipe ID to edit:").pack(anchor='w')
recipe_id_entry_edit = tk.Entry(edit_recipe_frame)
recipe_id_entry_edit.pack(anchor='w')

tk.Label(edit_recipe_frame, text="New Title:").pack(anchor='w')
title_entry_edit = tk.Entry(edit_recipe_frame)
title_entry_edit.pack(anchor='w')

tk.Label(edit_recipe_frame, text="New Category:").pack(anchor='w')
category_entry_edit = tk.Entry(edit_recipe_frame)
category_entry_edit.pack(anchor='w')

tk.Label(edit_recipe_frame, text="New Instructions:").pack(anchor='w')
instructions_text_edit = tk.Text(edit_recipe_frame, width=40, height=6)
instructions_text_edit.pack(anchor='w')

tk.Label(edit_recipe_frame, text="New Ingredients:").pack(anchor='w')
ingredients_text_edit = tk.Text(edit_recipe_frame, width=40, height=6)
ingredients_text_edit.pack(anchor='w')

tk.Button(edit_recipe_frame, text="Edit Recipe", command=edit_recipe_click, bg='yellow', fg='black').pack(pady=5)

# Search Recipe Frame
tk.Label(search_recipe_frame, text="Search Recipe", font=('Helvetica', 18, 'bold')).pack(pady=10)
tk.Button(search_recipe_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame), bg='teal', fg='white').pack(pady=5)

tk.Label(search_recipe_frame, text="Search recipes by category:").pack(anchor='w')
search_category_entry = tk.Entry(search_recipe_frame)
search_category_entry.pack(anchor='w')

tk.Button(search_recipe_frame, text="Search Recipe", command=search_recipe_click, bg='teal', fg='white').pack(pady=5)

# Show main menu on start
show_frame(main_menu_frame)

root.mainloop()

cursor.close()
conn.close()
