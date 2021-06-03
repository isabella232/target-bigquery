from tests import unittestcore


class TestComplexStreamLoadJob(unittestcore.BaseUnitTest):

    def test_klaviyo_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/klaviyo_stream.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")

    def test_recharge_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/recharge_stream.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")

    def test_bing_ads_stream(self):
        """
        data vs schema match here
        """
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/bing_ads_stream.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")

    def test_bing_ads_stream_data_vs_schema_dont_match(self):
        """
        This test succeeds

        It tests if we overcame the following error in Tap Bing Ads

        JSON schema library validator flags a mismatch in data type between data and schema.

        CRITICAL 123456 is not of type 'null', 'string'

        Failed validating 'type' in schema['properties']['BillToCustomerId']:
            {'type': ['null', 'string']}

        On instance['BillToCustomerId']:
            123456

        """

        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/bing_ads_stream_schema_vs_data_have_diff_data_types.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")


    def test_complex_stream(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/facebook_stream.json",
            config="../sandbox/target_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        # self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})
        #
        # table = self.client.get_table("{}.simple_stream_dev".format(self.dataset_id))
        # self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        # self.assertIsNone(table.clustering_fields)
        # self.assertIsNone(table.partitioning_type)

    def test_complex_stream_with_tables_config(self):
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/facebook_stream.json",
            config="../sandbox/target_config.json",
            tables="./rsc/facebook_stream_tables_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        # self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})
        #
        # table = self.client.get_table("{}.simple_stream_dev".format(self.dataset_id))
        # self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        # self.assertIsNotNone(table.clustering_fields)
        # self.assertIsNotNone(table.partitioning_type)


    def test_complex_stream_with_tables_config_force_field(self):
        """
        the purpose of this test is to make sure that if you supply date_start field in Facebook as string,
        build_schema function will force this field to date, according to target tables config file
        TODO: verify input and outputs:
        data type in input json schema, target tbl config force fields and resulting BQ tbl
        """

        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/facebook_stream_date_start_is_string.json",
            config="../sandbox/target_config.json",
            tables="./rsc/facebook_stream_tables_config.json",
            processhandler="load-job"
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
        # self.assertDictEqual(state, {"bookmarks": {"simple_stream": {"timestamp": "2020-01-11T00:00:00.000000Z"}}})
        #
        # table = self.client.get_table("{}.simple_stream_dev".format(self.dataset_id))
        # self.assertEqual(3, table.num_rows, msg="Number of rows mismatch")
        # self.assertIsNotNone(table.clustering_fields)
        # self.assertIsNotNone(table.partitioning_type)


    def test_misformed_complex_stream(self):
        """
        Note that the config's "validate_records" flag should be set to False
        """
        from target_bigquery import main

        self.set_cli_args(
            stdin="./rsc/facebook_stream.json",
            config="../sandbox/malformed_target_config.json",
            processhandler="load-job",
        )

        ret = main()
        state = self.get_state()[-1]
        print(state)

        self.assertEqual(ret, 0, msg="Exit code is not 0!")
