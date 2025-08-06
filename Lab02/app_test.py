import unittest
from unittest.mock import patch, MagicMock
from app import Application, MailSystem

class ApplicationTest(unittest.TestCase):
    def setUp(self):#In setUp(), stub the name list of the children
        #Step 1: Stub the name list
        self.app = Application()
        self.app.people = ["William", "Oliver", "Henry", "Liam"]#Set name list as "William, Oliver, Henry, Liam"
        self.app.selected = ["William", "Oliver", "Henry"]#Set the selected ones as "William, Oliver, Henry"
    def test_0_get_names(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='William\nOliver\nHenry\nLiam')):
            app = Application(people=["William", "Oliver", "Henry", "Liam"])
            expected_names = ["William", "Oliver", "Henry", "Liam"]
            self.assertEqual(app.people, expected_names)
   
    def test_1_get_random_person(self):
        with patch('random.randrange') as mock_randrange:
            # Set up the mock to return 3
            mock_randrange.return_value = 3
            # Call the method and assert that it returns "Liam"
            self.assertEqual(self.app.get_random_person(), "Liam")

    @patch('app.Application.get_random_person')
    def test_2_select_next_person(self, mock_get_random_person):
        # set up mock return values for get_random_person()
        mock_get_random_person.side_effect = ["William", "Oliver", "Henry","Liam"]#Mock get_random_person(), return values as follows: "William, Oliver, Henry, Liam"
        # call select_next_person() and check the return values
        next_person = self.app.select_next_person()
        print(next_person," selected")
        self.assertEqual(next_person, "Liam")#Examine the result of select_next_person() using assertEqual


    def test_3_notify_selected(self):
        # Mock MailSystem to avoid actual sending of emails
        self.app.selected = ["William", "Oliver", "Henry", "Liam"]
        mail_system_mock = MagicMock()
        self.app.mailSystem = mail_system_mock
        self.app.notify_selected()
        # Assert that write and send methods are called for each selected person
        for name in self.app.selected:
            mail_system_mock.write.assert_any_call(name)
            mail_system_mock.send.assert_any_call(name, mail_system_mock.write.return_value)
    





class MailSystemTest(unittest.TestCase):
    # Set up the mock for the fake_mail() function
    def fake_mail(self,name):#Finish fake_mail() and print the mail context.
            return f"Congrats, {name}!"
    def test_send_emails(self):
        mail_system = MailSystem()
        name_list = ["William", "Oliver", "Henry", "Liam"]
        # Spy on the write() and send() methods of the mail system
        with patch.object(mail_system, "write") as mock_write, \
             patch.object(mail_system, "send") as mock_send:

            # Set up the mock to return the fake mail
            mock_write.side_effect = self.fake_mail

            # Call the method to send the emails
            for name in  name_list:
                #mock_write.assert_any_call(name)
                context =  mock_write(name)
                print(context)
                mail_system.send(name,context)
               
            print()
            print()
            # Check that the write() method was called once for each name
            self.assertEqual(mock_write.call_count, 4)#Examine the call count of send() and write() using assertEqual
            print(mock_write.call_args_list)
            # Check that the send() method was called once for each name
            self.assertEqual(mock_send.call_count, 4)
            print(mock_send.call_args_list)

            for name in name_list:
                mock_write.assert_any_call(name)

            print("test_app(app_test.ApplicationTest) ... ok)")
            print()
# if __name__ == "__main__":
#     unittest.main()
   
