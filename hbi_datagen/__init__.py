import copy
import datetime
import uuid

from faker import Faker
from random import randint

name = "hbi_datagen"

fake = Faker()

UUID_KEYS = [
    "rhel_machine_id",
    "subscription_manager_id",
    "insights_id",
    "bios_uuid",
]

_DEFAULT_CLOUD_PROVIDER = "test cloud provider"

_DEFAULT_ANSIBLE_HOST = "default.test.redhat.com"


def generate_fqdn(panic_prevention="RHIQE"):
    return "{}.{}".format(panic_prevention, fake.hostname())


def generate_display_name(panic_prevention="RHIQE"):
    return "{}.{}".format(panic_prevention, fake.hostname())


def get_uuid_keys():
    return copy.deepcopy(UUID_KEYS)


def get_default_cloud_provider():
    return _DEFAULT_CLOUD_PROVIDER


def get_default_ansible_host():
    return _DEFAULT_ANSIBLE_HOST


def generate_ips(num_ips=2):
    """Generate a list of IPs."""
    result = []
    for i in range(0, num_ips):
        result.append(fake.ipv4_private())
    return result


def generate_facts(num_facts=2):
    """Generate some facts."""
    result = {"namespace": fake.domain_word(), "facts": {}}
    for i in range(0, num_facts):
        result["facts"][fake.domain_word()] = fake.domain_word()
    return result


def generate_macs(num_macs=2):
    """Generate a list of mac addresses."""
    result = []
    for i in range(0, num_macs):
        result.append(fake.mac_address())
    return result


def generate_tags():
    return []


def gen_iso8601_datetime(start_date="-10d", end_date="now"):
    """Generate a string containing datetime in correct ISO 8601 format, ending with "Z"."""
    return (
        fake.date_time_between(
            start_date=start_date, end_date=end_date, tzinfo=datetime.timezone.utc
        )
        .isoformat()
        .replace("+00:00", "Z")
    )


def create_system_profile_facts():
    return copy.deepcopy(_EXAMPLE_SYSTEM_PROFILE_FACTS)


def create_host_data(
    account_number, extra_data=None, include_sysprofile=True, panic_prevention="RHIQE"
):
    if include_sysprofile:
        data = copy.deepcopy(_EXAMPLE_PAYLOAD_WITH_PROFILE_FACTS)
    else:
        data = copy.deepcopy(_EXAMPLE_PAYLOAD)

    identifiers = uuid.uuid4().hex

    data["account"] = str(account_number)
    for uuid_key in UUID_KEYS:
        data[uuid_key] = identifiers

    if fake.pybool():
        data['satellite_id'] = identifiers

    data["display_name"] = generate_display_name(panic_prevention)
    data["ansible_host"] = fake.hostname()
    data["fqdn"] = generate_fqdn(panic_prevention)

    data["ip_addresses"] = generate_ips()
    data["mac_addresses"] = generate_macs()

    data["facts"] = [generate_facts()]
    # TODO: Generate Tags

    data['stale_timestamp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=randint(1, 7))
    data['reporter'] = fake.pystr()

    data = {**data, **extra_data} if extra_data and isinstance(extra_data, dict) else data

    return data


_EXAMPLE_SYSTEM_PROFILE_FACTS = {
    "arch": "string",
    "bios_release_date": "string",
    "bios_vendor": "string",
    "bios_version": "string",
    "cloud_provider": _DEFAULT_CLOUD_PROVIDER,
    "cores_per_socket": 2,
    "cpu_flags": [],
    "disk_devices": [],
    "enabled_services": [],
    "infrastructure_type": "string",
    "infrastructure_vendor": "string",
    "insights_client_version": "string",
    "insights_egg_version": "string",
    "installed_packages": [],
    "installed_products": [],
    "installed_services": [],
    "katello_agent_running": False,
    "kernel_modules": [],
    "last_boot_time": gen_iso8601_datetime(),
    "network_interfaces": [],
    "number_of_cpus": 4,
    "number_of_sockets": 1,
    "os_kernel_version": "string",
    "os_release": "string",
    "running_processes": [],
    "satellite_managed": True,
    "subscription_auto_attach": "string",
    "subscription_status": "string",
    "system_memory_bytes": 3,
    "yum_repos": [],
}
_EXAMPLE_PAYLOAD = {
    "ansible_host": _DEFAULT_ANSIBLE_HOST,
    "display_name": "new.mydomain.com",
    "account": "10203040",
    "insights_id": "40ec059615724ebab7521463757b66a2",
    "rhel_machine_id": "40ec059615724ebab7521463757b66a2",
    "subscription_manager_id": "40ec059615724ebab7521463757b66a2",
    "bios_uuid": "40ec059615724ebab7521463757b66a2",
    "ip_addresses": ["10.10.0.1", "10.0.0.2"],
    "fqdn": "some.host.example.com",
    "mac_addresses": ["c2:00:d0:c8:61:01"],
    "facts": [
        {"namespace": "string", "facts": {"fact1": "fact_number_one", "fact2": "fact_number_two"}}
    ],
    "tags": [],
}
_EXAMPLE_PAYLOAD_WITH_PROFILE_FACTS = copy.deepcopy(_EXAMPLE_PAYLOAD)
_EXAMPLE_PAYLOAD_WITH_PROFILE_FACTS["system_profile"] = _EXAMPLE_SYSTEM_PROFILE_FACTS
