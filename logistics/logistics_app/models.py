from django.db import models

# Create your models here.

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


'''
###################################### МОДЕЛИ ###########################################
'''


class Application(models.Model):
    name = models.CharField(max_length=200)
    isinprogress = models.BooleanField(db_column='isInProgress')  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    finishdate = models.DateField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey('Branch', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application'
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return f"{self.name} {self.startdate} ({self.id})"


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return f"{self.name} {self.address} ({self.id})"


class Car(models.Model):
    number = models.CharField(max_length=8)
    isinsured = models.BooleanField(db_column='isInsured')  # Field name made lowercase.
    mileage = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    carlist = models.ForeignKey('Carlist', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car'
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f"{self.number} ({self.id})"


class Cargo(models.Model):
    weight = models.FloatField()
    length = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    isspecific = models.BooleanField(db_column='isSpecific')  # Field name made lowercase.
    application = models.ForeignKey(Application, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('Type', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargo'
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'

    def __str__(self):
        return f"Груз номер: {self.id}"


class Carlist(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    volume = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carlist'
        verbose_name = 'Автопарк'
        verbose_name_plural = 'Список автомобилей'

    def __str__(self):
        return f"{self.name}-{self.manufacturer.name} ({self.id})"


class Clients(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    passport_series = models.CharField(max_length=4)
    passport_number = models.CharField(max_length=6)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12)
    passed = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.id})"


class Contact(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=32)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=32)  # Field name made lowercase.
    phone = models.CharField(max_length=12)
    organization = models.CharField(max_length=100, blank=True, null=True)
    application = models.ForeignKey(Application, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.id})"


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f"{self.name} {self.country} ({self.id})"


class OngoingPassage(models.Model):
    departuredate = models.DateField(db_column='departureDate', blank=True, null=True)  # Field name made lowercase.
    arrivaldate = models.DateField(db_column='arrivalDate', blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.BooleanField(db_column='isCompleted')  # Field name made lowercase.
    car = models.ForeignKey(Car, models.DO_NOTHING)
    worker = models.ForeignKey('Worker', models.DO_NOTHING, related_name='worker_passage_set_now')
    loader = models.ForeignKey('Worker', models.DO_NOTHING, blank=True, null=True, related_name='loader_passage_set_now')

    class Meta:
        managed = False
        db_table = 'ongoing_passage'
        verbose_name = 'Активный рейс'
        verbose_name_plural = 'Активные рейсы'

    def __str__(self):
        return f"{self.iscompleted} ({self.id})"


class Orders(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    conclusion_date = models.DateField()
    payment_type = models.CharField(max_length=20)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    prop = models.ForeignKey('Prop', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ номер: {self.id}"


class Parking(models.Model):
    isdamaged = models.BooleanField(db_column='isDamaged')  # Field name made lowercase.
    number = models.CharField(max_length=12, blank=True, null=True)
    carlist = models.ForeignKey(Carlist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parking'
        verbose_name = 'Стоянка'
        verbose_name_plural = 'Стоянки'

    def __str__(self):
        return f"Стоянка: {self.number}"


class Passage(models.Model):
    departuredate = models.DateField(db_column='departureDate', blank=True, null=True)  # Field name made lowercase.
    arrivaldate = models.DateField(db_column='arrivalDate', blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.BooleanField(db_column='isCompleted')  # Field name made lowercase.
    car = models.ForeignKey(Car, models.DO_NOTHING)
    worker = models.ForeignKey('Worker', models.DO_NOTHING, related_name='worker_passage_set')
    loader = models.ForeignKey('Worker', models.DO_NOTHING, blank=True, null=True, related_name='loader_passage_set')
    application = models.ForeignKey(Application, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'passage'
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    def __str__(self):
        return f"Рейс номер: {self.id} | {self.departuredate}"


class Prop(models.Model):
    bankname = models.CharField(db_column='bankName', max_length=100)  # Field name made lowercase.
    bankaccount = models.CharField(db_column='bankAccount', max_length=100)  # Field name made lowercase.
    bik = models.CharField(max_length=100, blank=True, null=True)
    kpp = models.CharField(max_length=100, blank=True, null=True)
    inn = models.CharField(max_length=100, blank=True, null=True)
    ks = models.CharField(max_length=100, blank=True, null=True)
    rs = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prop'
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return f"{self.bankname} - {self.bankaccount}"


class Route(models.Model):
    shipping_address = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    distance = models.FloatField(blank=True, null=True)
    estimated_time = models.IntegerField(blank=True, null=True)
    application = models.ForeignKey(Application, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f"Маршрут номер: {self.id} | {self.delivery_address}"


class Type(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return f"{self.name} | {self.number}"


class Worker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    passport_series = models.CharField(max_length=4)
    passport_number = models.CharField(max_length=6)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12)
    isworking = models.BooleanField(db_column='isWorking', blank=True, null=True)  # Field name made lowercase.
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker'
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return f"{self.last_name} | {self.first_name}"


class PaymentsView(models.Model):
    payment_type = models.CharField(db_column="payment_type", max_length=20, primary_key=True, verbose_name='Способ оплаты')
    payment_ru = models.TextField(db_column="payment_ru", verbose_name='Способ оплаты (рус.)')
    average = models.FloatField(db_column="average", verbose_name='Средний чек (рубли)')

    class Meta:
        managed = False
        db_table = 'payments'
        verbose_name = 'Средний чек по способу оплаты'
        verbose_name_plural = 'Средние чеки по способам оплаты'

    def __str__(self):
        return f"{self.payment_ru}:     {self.average} (рубли)"
