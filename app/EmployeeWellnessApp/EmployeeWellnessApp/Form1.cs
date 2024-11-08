using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Runtime.Remoting.Contexts;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Health_Management_System;
using MySql.Data.MySqlClient;

namespace EmployeeWellnessApp
{
    public partial class LoginPage : Form
    {
        private DataBaseConnection connect;

        public LoginPage()
        {
            InitializeComponent();
        }

        private void button_close_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void username_TextChanged(object sender, EventArgs e)
        {

        }

        private void password_TextChanged(object sender, EventArgs e)
        {
            password.UseSystemPasswordChar = false;
        }

        private void Login_button_Click(object sender, EventArgs e)
        {
            if (username.Text.Trim().Equals("") || password.Text == "")
            {
                MessageBox.Show("Enter your username and password", "Missing Login Information", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            else
            {

                if (username.Text.Trim().StartsWith("Manager"))
                {
                    DataTable table = new DataTable();
                    MySqlDataAdapter adapter = new MySqlDataAdapter();
                    string selectquerry = "SELECT * FROM `manager` WHERE `managerUsername` = @usn AND `managerPassword` = @pass";
                    MySqlCommand command = new MySqlCommand(selectquerry, connect.GetConnection());
                    command.Parameters.Add("@usn", MySqlDbType.VarChar).Value = username.Text;
                    command.Parameters.Add("@pass", MySqlDbType.VarChar).Value = password.Text;
                    adapter.SelectCommand = command;
                    adapter.Fill(table);
                    if (table.Rows.Count > 0)
                    {
                        this.Hide();
                        ManagerForm mainForm = new ManagerForm();
                        mainForm.Show();
                    }
                    else
                    {
                        MessageBox.Show("Your username and Password doesn't exists", "Wrong Login Information", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                else
                {
                    DataTable table = new DataTable();
                    MySqlDataAdapter adapter = new MySqlDataAdapter();
                    string selectquerry = "SELECT * FROM `users` WHERE `username` = @usn AND `password` = @pass";
                    MySqlCommand command = new MySqlCommand(selectquerry, connect.GetConnection());
                    command.Parameters.Add("@usn", MySqlDbType.VarChar).Value = username.Text;
                    command.Parameters.Add("@pass", MySqlDbType.VarChar).Value = password.Text;
                    adapter.SelectCommand = command;
                    adapter.Fill(table);
                    if (table.Rows.Count > 0)
                    {
                        this.Hide();
                        UserForm mainFormClient = new UserForm();
                        mainFormClient.Show();
                    }
                    else
                    {
                        MessageBox.Show("Your username and Password doesn't exists", "Wrong Login Information", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }

            }
        }
    }
}
