# Property Management

![Property Management](https://img.shields.io/badge/Property_Management-v0.0.1-blue)
![Frappe](https://img.shields.io/badge/Built%20with-Frappe-green)
![ERPNext](https://img.shields.io/badge/Powered%20by-ERPNext-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

A comprehensive property management system built on the Frappe Framework and ERPNext platform. This app provides end-to-end solutions for real estate operations, from property portfolio management to tenant relations and maintenance tracking.

## Overview

Property Management is a fully-featured application designed to streamline real estate operations by leveraging the power of ERPNext's robust infrastructure. Built on Frappe Framework v15 and ERPNext v15, this app provides seamless integration with accounting, CRM, and inventory management modules.

### Key Features

- **Property Portfolio Management**: Complete hierarchy from projects to individual units
- **Tenant Management**: Comprehensive tenant profiles and relationship tracking
- **Lease Management**: Automated tenancy agreements with rent tracking
- **Maintenance & Service Requests**: Streamlined maintenance request workflow
- **Utility Management**: Meter readings and utility billing automation
- **Financial Integration**: Seamless accounting and invoicing
- **Advanced Analytics**: Real-time dashboards and reporting
- **Role-Based Access**: Granular permissions for different user roles

## Architecture

### Built on Frappe Framework

This app leverages Frappe's powerful framework capabilities:

- **DocType System**: Custom data structures for property entities
- **Workflow Engine**: Automated business processes
- **Permission System**: Role-based access control
- **API Framework**: RESTful APIs for integration
- **Reporting Engine**: Custom reports and analytics
- **Notification System**: Automated alerts and communications

### ERPNext Integration

Deep integration with ERPNext modules provides enterprise-grade functionality:

- **Accounting Module**: Automatic rent invoicing and payment tracking
- **CRM Module**: Tenant relationship management
- **Inventory Module**: Asset tracking for utilities and maintenance
- **Projects Module**: Property development tracking
- **HR Module**: Staff and contractor management

## Core DocTypes

### Property Hierarchy
- **Property Project**: Master record for real estate developments
- **Building**: Individual buildings within projects
- **Floor**: Floor levels within buildings
- **Unit**: Individual rental units (apartments, offices, shops)

### Tenant Management
- **Tenant Profile**: Complete tenant information with verification
- **Tenancy**: Lease agreements and rental terms
- **Rent History**: Historical rent payment tracking

### Operations Management
- **Service Request**: Maintenance and repair requests
- **Utility Meter**: Water, electricity, gas meter management
- **Meter Reading**: Periodic meter readings and consumption tracking

### Supporting Entities
- **Building Amenity**: Shared facilities management
- **Unit Amenity**: Individual unit features
- **Service Request Attachment**: Document management for requests

## Key Workflows

### 1. Property Setup Workflow
```
Property Project -> Building -> Floor -> Unit
```

### 2. Tenant Onboarding
```
Tenant Profile -> Tenancy Agreement -> Unit Assignment
```

### 3. Maintenance Management
```
Service Request -> Assignment -> Resolution -> Cost Tracking
```

### 4. Utility Billing
```
Meter Installation -> Reading -> Consumption Calculation -> Invoice Generation
```

## Dashboard & Analytics

### Modern Workspace Interface
- **Property Portfolio Overview**: Visual dashboard with key metrics
- **Real-time KPIs**: Total properties, active tenancies, available units
- **Revenue Analytics**: Monthly rental income trends
- **Service Metrics**: Open maintenance requests tracking

### Number Cards
- **Total Properties**: Complete property count
- **Active Tenancies**: Current lease agreements
- **Available Units**: Ready-to-rent units
- **Monthly Rental Income**: Revenue tracking
- **Open Service Requests**: Maintenance workload

### Charts & Reports
- **Property Portfolio Distribution**: Donut chart by status
- **Rental Income Trends**: Time-series revenue analysis
- **Maintenance Summary**: Service request analytics
- **Rent Collection Reports**: Payment tracking

## Technical Features

### Automated Processes
- **Rent Calculation**: Automatic rent amount computation
- **Lease Expiry Alerts**: Proactive lease management
- **Maintenance Notifications**: Automated service request alerts
- **Utility Billing**: Automated invoice generation

### Data Validation
- **Unit Status Management**: Automatic status updates
- **Tenant Verification**: ID proof validation
- **Duplicate Prevention**: Unique identifier enforcement
- **Financial Controls**: Accounting integration validation

### Integration Capabilities
- **ERPNext Accounting**: Seamless financial management
- **Email Integration**: Automated notifications
- **File Management**: Document attachment system
- **API Access**: RESTful endpoints for external systems

## Installation

### Prerequisites
- Frappe Framework v15.88.2+
- ERPNext v15.88.1+
- MariaDB 10.6+
- Node.js 16+
- Python 3.11+

### Installation Steps

1. **Clone the Repository**
```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/Ascra-Tech/property_management.git --branch develop
```

2. **Install the App**
```bash
bench install-app property_management
```

3. **Migrate Database**
```bash
bench --site your.site.name migrate
```

4. **Restart Services**
```bash
bench restart
```

### Post-Installation Setup

1. **Create Property Manager Role**
2. **Set Up Property Projects**
3. **Configure Building and Unit Hierarchies**
4. **Create Tenant Profiles**
5. **Set Up Utility Meters**

## Configuration

### Role-Based Access
- **Property Manager**: Full system access
- **Property Staff**: Limited operational access
- **Tenant**: View-only access to personal information

### Customization Options
- **Naming Series**: Configurable numbering patterns
- **Status Workflows**: Custom status transitions
- **Email Templates**: Branded communication templates
- **Report Formats**: Custom report layouts

## API & Integration

### REST APIs
The app provides comprehensive REST APIs for:
- Property management operations
- Tenant data access
- Maintenance request management
- Financial data integration

### Webhooks
- Lease expiry notifications
- Rent payment confirmations
- Maintenance request updates
- Utility billing events

## Development

### App Structure
```
property_management/
property_management/          # Main app module
  doctype/                   # Custom DocTypes
  workspace/                 # Dashboard configurations
  dashboard_chart_source/    # Analytics charts
  number_card/              # KPI cards
  install.py                # Installation scripts
  hooks.py                  # Frappe hooks
  tasks.py                  # Scheduled tasks
```

### Extending the App
- **Custom DocTypes**: Add new property entities
- **Custom Reports**: Create specialized analytics
- **Workflow Extensions**: Enhance business processes
- **API Integrations**: Connect external systems

### Contributing Guidelines

1. **Code Standards**
   - Follow Frappe coding conventions
   - Use meaningful variable names
   - Add comprehensive docstrings

2. **Testing**
   - Write unit tests for new features
   - Test with sample data
   - Verify ERPNext integration

3. **Documentation**
   - Update README for new features
   - Document API changes
   - Maintain changelog

## Support & Maintenance

### Scheduled Tasks
- **Lease Expiry Checks**: Daily monitoring
- **Rent Reminders**: Monthly notifications
- **Maintenance Reports**: Weekly summaries
- **Property Valuation**: Periodic updates

### Troubleshooting
- **Common Issues**: FAQ section
- **Error Logs**: System diagnostics
- **Performance**: Optimization tips

## Roadmap

### Upcoming Features
- **Mobile App**: Native mobile application
- **Advanced Analytics**: AI-powered insights
- **Multi-Currency Support**: International operations
- **IoT Integration**: Smart building features

### Version History
- **v0.0.1**: Initial release with core functionality
- **v0.1.0**: Enhanced analytics and reporting
- **v0.2.0**: Mobile app integration (planned)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Wiki](https://github.com/Ascra-Tech/property_management/wiki)
- **Issues**: [GitHub Issues](https://github.com/Ascra-Tech/property_management/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ascra-Tech/property_management/discussions)
- **Email**: amit@ascratech.com

## About Ascra Tech

Ascra Tech specializes in developing enterprise solutions on the Frappe Framework. Our expertise includes:

- **Custom ERP Development**
- **Mobile App Integration**
- **Cloud Deployment Solutions**
- **API Development & Integration**

Visit our website: [ascratech.com](https://ascratech.com)

---

**Built with passion for property management excellence** | **Powered by Frappe & ERPNext**
