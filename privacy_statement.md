# Personal Data Handling and Privacy Strategy

## Personal Data Collected and Processed
The Green Academy API handles the following categories of personal data:
- **User Profile Data:**
  - Username
  - Email address
  - First name
  - Last name
  - Date joined
  - Account status (active/inactive, staff/admin)
- **Enrollment Data:**
  - Associations between users and courses (enrollments)
  - Enrollment status and completion percentage
- **Authentication Data:**
  - Passwords (securely hashed, never stored in plaintext)
  - JWT tokens for session management

## Privacy and Data Protection Strategy
The API is designed with privacy and data protection in mind, following GDPR and other relevant regulations:

### 1. **Data Minimization & Access Control**
- Only necessary personal data is collected and processed.
- Access to personal data is restricted:
  - Users can only access, export, or delete their own data (except for admins).
  - Admins can manage all user data for legitimate purposes.

### 2. **User Rights**
- **Right to Access:**
  - Users can retrieve their own data via the `/users/me/` endpoint.
- **Right to Data Portability:**
  - Users can export their personal data via the `/users/me/export/` endpoint.
- **Right to Erasure ("Right to be Forgotten"):**
  - Users can delete their account and associated personal data via the `/users/me/delete/` endpoint.

### 3. **Security Measures**
- Passwords are securely hashed using Django's password management system.
- JWT authentication is used to protect sensitive endpoints.
- Data is only transmitted over secure HTTPS connections (in production).

### 4. **Data Retention and Deletion**
- When a user deletes their account, all associated personal data is permanently removed from the database.
- No personal data is retained after account deletion unless required by law.

### 5. **Compliance and Transparency**
- The API is documented to clearly indicate which endpoints handle personal data and the user's rights.
- Privacy features are visible in the Swagger/OpenAPI documentation.