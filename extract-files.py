#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/sm7250-common',
    'hardware/qcom-caf/sm8250',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-vendor' if partition in 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    (
        'libqsap_sdk',
        'libril',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup()
        .regex_replace('system/framework', 'system/system_ext/framework'),
    ('system_ext/etc/permissions/vendor.qti.hardware.data.connection-V1.0-java.xml', 'system_ext/etc/permissions/vendor.qti.hardware.data.connection-V1.1-java.xml'): blob_fixup()
        .regex_replace('xml version="2.0"', 'xml version="1.0"')
        .regex_replace('/product/', '/system_ext/'),
    ('system_ext/lib/lib-imsvideocodec.so', 'system_ext/lib64/lib-imsvideocodec.so'): blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/priv-app/ims/ims.apk': blob_fixup()
        .apktool_patch('ims-patches'),
    'vendor/etc/permissions/com.motorola.androidx.camera.extensions.xml': blob_fixup()
        .regex_replace('system_ext', 'product'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
# Dolby START
    'odm/bin/hw/vendor.dolby_sp.media.c2@1.0-service': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0_sp.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk_sp.so'),
    'odm/lib64/libcodec2_store_dolby_sp.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk_sp.so'),
    ('odm/lib64/libcodec2_soft_ac4dec_sp.so', 'odm/lib64/libcodec2_soft_ddpdec_sp.so'): blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk_sp.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common_sp.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    ('odm/lib64/libcodec2_soft_common_sp.so', 'odm/lib64/libcodec2_hidl_plugin_sp.so'): blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk_sp.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    (
        'odm/lib/libdlbdsservice_v3_6.so',
        'odm/lib/libstagefright_soft_ddpdec.so',
        'odm/lib64/libdlbdsservice_sp.so',
        'odm/lib64/libdlbdsservice_v3_6.so'
    ): blob_fixup().replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'odm/lib64/libcodec2_vndk_sp.so': blob_fixup()
        .replace_needed('libui.so', 'libui_sp.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'odm/lib64/libcodec2_hidl@1.0_sp.so': blob_fixup()
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin_sp.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk_sp.so'),
    'odm/lib64/libui_sp.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V6-ndk.so')
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so'),
    # Dolby END
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7250-common',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
