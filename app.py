import pymongo
import streamlit as st


# Connect to the MongoDB client
client = pymongo.MongoClient()
db = client['library']
books_col = db['books']


# Define the Streamlit app
def app():
    # Set the page title
    st.set_page_config(page_title='Library Catalog')

    # Display the page title
    st.title('Library Catalog')

    # Define the form for inserting new details
    st.header('Insert New Details')
    with st.form(key='insert_form'):
        title = st.text_input('Title')
        author = st.text_input('Author')
        status = st.selectbox('Status', options=['available', 'checked out'])

        if st.form_submit_button(label='Insert'):
            # Insert the new book into the database
            book_id = books_col.insert_one({
                'title': title,
                'author': author,
                'status': status
            }).inserted_id

            st.success(f'New book added with id {book_id}')

    # Define the section for viewing details
    st.header('View Details')
    view_type = st.selectbox('Select view type', options=['All', 'Individual'])
    if view_type == 'All':
        books = list(books_col.find())
        st.table(books)
    else:
        book_title = st.text_input('Enter book title')
        if book_title:
            books = list(books_col.find({'title': book_title}))
            if books:
                st.table(books)
            else:
                st.error('No books found with that title')

    # Define the section for updating details
    st.header('Update Details')
    with st.form(key='update_form'):
        book_title = st.text_input('Enter book title')
        author = st.text_input('Author')
        status = st.selectbox('Status', options=['available', 'checked out'])
        if st.form_submit_button(label='Update'):
            # Update the book status in the database
            result = books_col.update_many({'title': book_title}, {'$set': {'author': author,'status': status}})
            if result.modified_count > 0:
                st.success(f'{result.modified_count} books updated')
            else:
                st.error('No books found with that title')

    # Define the section for deleting details
    st.header('Delete Details')
    with st.form(key='delete_form'):
        book_title = st.text_input('Enter book title')
        if st.form_submit_button(label='Delete'):
            # Delete the book from the database
            result = books_col.delete_many({'title': book_title})
            if result.deleted_count > 0:
                st.success(f'{result.deleted_count} books deleted')
            else:
                st.error('No books found with that title')


if __name__ == '__main__':
    app()
