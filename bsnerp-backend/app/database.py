from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os

class InMemoryDatabase:
    def __init__(self):
        self.users: Dict[int, Dict] = {}
        self.clients: Dict[int, Dict] = {}
        self.projects: Dict[int, Dict] = {}
        self.tasks: Dict[int, Dict] = {}
        self.transactions: Dict[int, Dict] = {}
        self.categories: Dict[int, Dict] = {}
        self.invoices: Dict[int, Dict] = {}
        self.servers: Dict[int, Dict] = {}
        self.credentials: Dict[int, Dict] = {}
        self.notifications: Dict[int, Dict] = {}
        self.notification_templates: Dict[int, Dict] = {}
        self.notification_subscriptions: Dict[int, Dict] = {}
        self.backup_records: Dict[int, Dict] = {}
        self.maintenance_records: Dict[int, Dict] = {}
        
        self._counters = {
            'users': 0,
            'clients': 0,
            'projects': 0,
            'tasks': 0,
            'transactions': 0,
            'categories': 0,
            'invoices': 0,
            'servers': 0,
            'credentials': 0,
            'notifications': 0,
            'notification_templates': 0,
            'notification_subscriptions': 0,
            'backup_records': 0,
            'maintenance_records': 0,
        }
        
        self._initialize_sample_data()
    
    def _get_next_id(self, table: str) -> int:
        self._counters[table] += 1
        return self._counters[table]
    
    def _initialize_sample_data(self):
        now = datetime.now()
        
        admin_user = {
            'id': self._get_next_id('users'),
            'email': 'admin@bsnerp.com',
            'username': 'admin',
            'full_name': 'مدير النظام',
            'phone': '+201234567890',
            'role': 'admin',
            'status': 'active',
            'avatar': None,
            'department': 'إدارة',
            'position': 'مدير عام',
            'skills': ['إدارة', 'قيادة', 'تخطيط'],
            'permissions': ['all'],
            'two_factor_enabled': False,
            'two_factor_secret': None,
            'last_login': now,
            'created_at': now,
            'updated_at': now,
            'password_hash': '$2b$12$HskPFh4SPtblDVTOom4VGeng3N2RCGOCCK1Nr6Z5n55UKCFHv0jT6',
            'reset_token': None,
            'reset_token_expires': None,
            'email_verified': True,
            'verification_token': None
        }
        self.users[admin_user['id']] = admin_user
        
        sample_client = {
            'id': self._get_next_id('clients'),
            'name': 'شركة التقنية المتقدمة',
            'email': 'info@techadvanced.com',
            'phone': '+201111111111',
            'type': 'company',
            'status': 'active',
            'company_name': 'شركة التقنية المتقدمة للحلول الرقمية',
            'website': 'https://techadvanced.com',
            'address': 'القاهرة الجديدة، مصر',
            'city': 'القاهرة',
            'country': 'مصر',
            'tax_number': '123456789',
            'contact_persons': [
                {
                    'name': 'أحمد محمد',
                    'email': 'ahmed@techadvanced.com',
                    'phone': '+201111111111',
                    'position': 'مدير التسويق',
                    'is_primary': True
                }
            ],
            'notes': 'عميل مهم يحتاج متابعة خاصة',
            'tags': ['vip', 'تقنية'],
            'source': 'موقع الشركة',
            'assigned_manager': admin_user['id'],
            'total_projects': 2,
            'total_revenue': 50000.0,
            'last_project_date': now,
            'documents': [],
            'custom_fields': {},
            'created_at': now,
            'updated_at': now
        }
        self.clients[sample_client['id']] = sample_client
        
        sample_project = {
            'id': self._get_next_id('projects'),
            'name': 'موقع شركة التقنية المتقدمة',
            'description': 'تطوير موقع إلكتروني متجاوب لشركة التقنية المتقدمة',
            'client_id': sample_client['id'],
            'type': 'website',
            'status': 'in_progress',
            'priority': 'high',
            'start_date': now,
            'end_date': None,
            'estimated_hours': 120.0,
            'actual_hours': 45.0,
            'budget': 25000.0,
            'actual_cost': 11250.0,
            'progress': 37.5,
            'phases': [
                {
                    'id': 1,
                    'name': 'التخطيط والتصميم',
                    'description': 'مرحلة التخطيط وتصميم الواجهات',
                    'start_date': now,
                    'end_date': None,
                    'status': 'completed',
                    'progress': 100.0,
                    'budget': 8000.0,
                    'actual_cost': 8000.0,
                    'deliverables': ['تصميم الواجهات', 'خريطة الموقع']
                },
                {
                    'id': 2,
                    'name': 'التطوير',
                    'description': 'مرحلة تطوير الموقع',
                    'start_date': now,
                    'end_date': None,
                    'status': 'in_progress',
                    'progress': 60.0,
                    'budget': 15000.0,
                    'actual_cost': 9000.0,
                    'deliverables': ['الصفحة الرئيسية', 'صفحات المنتجات']
                }
            ],
            'team_members': [
                {
                    'user_id': admin_user['id'],
                    'role': 'مدير المشروع',
                    'hourly_rate': 250.0,
                    'allocated_hours': 40.0,
                    'actual_hours': 15.0
                }
            ],
            'tags': ['موقع', 'شركة'],
            'files': [],
            'notes': 'مشروع مهم يحتاج متابعة يومية',
            'requirements': 'موقع متجاوب مع لوحة تحكم إدارية',
            'deliverables': ['موقع كامل', 'لوحة تحكم', 'دليل المستخدم'],
            'milestones': [],
            'risks': [],
            'custom_fields': {},
            'template_id': None,
            'parent_project_id': None,
            'created_at': now,
            'updated_at': now
        }
        self.projects[sample_project['id']] = sample_project
        
        sample_task = {
            'id': self._get_next_id('tasks'),
            'title': 'تصميم الصفحة الرئيسية',
            'description': 'تصميم وتطوير الصفحة الرئيسية للموقع',
            'project_id': sample_project['id'],
            'assigned_to': admin_user['id'],
            'created_by': admin_user['id'],
            'status': 'in_progress',
            'priority': 'high',
            'type': 'design',
            'estimated_hours': 8.0,
            'actual_hours': 3.0,
            'due_date': now,
            'start_date': now,
            'completed_at': None,
            'tags': ['تصميم', 'صفحة رئيسية'],
            'attachments': [],
            'subtasks': [],
            'comments': [],
            'time_entries': [],
            'dependencies': [],
            'watchers': [admin_user['id']],
            'custom_fields': {},
            'kanban_position': 1,
            'recurring': False,
            'recurring_pattern': None,
            'parent_task_id': None,
            'created_at': now,
            'updated_at': now
        }
        self.tasks[sample_task['id']] = sample_task
        
        income_category = {
            'id': self._get_next_id('categories'),
            'name': 'إيرادات المشاريع',
            'type': 'income',
            'parent_id': None,
            'color': '#10B981',
            'icon': 'trending-up',
            'budget_limit': None,
            'created_at': now
        }
        self.categories[income_category['id']] = income_category
        
        expense_category = {
            'id': self._get_next_id('categories'),
            'name': 'مصاريف التشغيل',
            'type': 'expense',
            'parent_id': None,
            'color': '#EF4444',
            'icon': 'trending-down',
            'budget_limit': 10000.0,
            'created_at': now
        }
        self.categories[expense_category['id']] = expense_category
        
        sample_transaction = {
            'id': self._get_next_id('transactions'),
            'type': 'income',
            'amount': 12500.0,
            'currency': 'EGP',
            'description': 'دفعة أولى من مشروع موقع شركة التقنية المتقدمة',
            'category_id': income_category['id'],
            'project_id': sample_project['id'],
            'client_id': sample_client['id'],
            'invoice_id': None,
            'status': 'approved',
            'payment_method': 'bank_transfer',
            'reference_number': 'TXN-001',
            'receipt_file': None,
            'notes': 'تم استلام المبلغ بنجاح',
            'tags': ['دفعة أولى'],
            'recurring': False,
            'recurrence_pattern': 'none',
            'recurrence_end_date': None,
            'parent_transaction_id': None,
            'approved_by': admin_user['id'],
            'approved_at': now,
            'transaction_date': now,
            'created_at': now,
            'updated_at': now
        }
        self.transactions[sample_transaction['id']] = sample_transaction
        
        sample_server = {
            'id': self._get_next_id('servers'),
            'name': 'خادم الإنتاج الرئيسي',
            'hostname': 'prod-server-01.bsnerp.com',
            'ip_address': '192.168.1.100',
            'type': 'web',
            'status': 'online',
            'provider': 'Hostinger',
            'location': 'مصر',
            'specifications': {
                'cpu': '4 cores',
                'ram': '8GB',
                'storage': '100GB SSD',
                'bandwidth': '1TB'
            },
            'monthly_cost': 500.0,
            'ssh_port': 22,
            'ssh_username': 'root',
            'ssh_key_path': '/keys/prod-server.pem',
            'monitoring_enabled': True,
            'backup_enabled': True,
            'backup_schedule': 'daily',
            'last_backup': now,
            'uptime_percentage': 99.9,
            'cpu_usage': 45.2,
            'memory_usage': 62.8,
            'disk_usage': 34.5,
            'network_in': 1024.5,
            'network_out': 2048.3,
            'installed_software': ['Apache', 'MySQL', 'PHP', 'WordPress'],
            'security_updates': [],
            'ssl_certificates': [
                {
                    'domain': 'bsnerp.com',
                    'issuer': 'Let\'s Encrypt',
                    'expires_at': '2025-12-31'
                }
            ],
            'projects': [sample_project['id']],
            'notes': 'خادم مهم يحتاج مراقبة مستمرة',
            'tags': ['إنتاج', 'مهم'],
            'created_at': now,
            'updated_at': now
        }
        self.servers[sample_server['id']] = sample_server

db = InMemoryDatabase()
